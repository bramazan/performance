#!/usr/bin/env python3
"""
Jira Team Analysis for Service Banking
Analyzes team's work in Jira for 2025:
- Story points completed
- Issue types distribution
- Completion rates
- Sprint performance
- Team velocity
"""

import os
import sys
from datetime import datetime
import pandas as pd
from jira import JIRA
import re
from collections import defaultdict


def parse_jira_env(env_file='jira.env'):
    """Parse jira.env file"""
    config = {}

    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                config[key.strip()] = value.strip()

    # Extract server from link
    if 'Jira_Link' in config:
        link = config['Jira_Link']
        # Extract base URL (https://ode-al.atlassian.net)
        match = re.match(r'(https://[^/]+)', link)
        if match:
            config['JIRA_SERVER'] = match.group(1)

        # Extract project key from link (TSB)
        if '/projects/' in link:
            project = link.split('/projects/')[1].split('/')[0]
            config['PROJECT_KEY'] = project

    return config


def analyze_jira_team(api_token: str, jira_server: str, project_key: str,
                      start_date: str = '2025-01-01', end_date: str = '2025-12-31',
                      config: dict = None):
    """
    Analyze team's Jira performance

    Args:
        api_token: Jira API token
        jira_server: Jira server URL
        project_key: Project key (e.g., 'TSB')
        start_date: Analysis start date
        end_date: Analysis end date
    """

    print(f"\n{'='*100}")
    print(f"🎯 JIRA TEAM ANALYSIS: {project_key}")
    print(f"📅 Period: {start_date} to {end_date}")
    print(f"🔗 Server: {jira_server}")
    print(f"{'='*100}\n")

    # Connect to Jira
    # For Atlassian Cloud, use email as username
    print("🔌 Connecting to Jira...")

    # Check if EMAIL is provided in config
    email = config.get('EMAIL', None)

    try:
        # Use basic auth with email + API token for Atlassian Cloud
        # Force API version 3
        options = {
            'server': jira_server,
            'rest_api_version': '3'  # Use API v3
        }

        if email:
            jira = JIRA(
                options=options,
                basic_auth=(email, api_token)
            )
        else:
            jira = JIRA(
                options=options,
                token_auth=api_token
            )
        print("✅ Connected to Jira successfully (API v3)!\n")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("\n💡 For Atlassian Cloud, add EMAIL to jira.env:")
        print("   EMAIL: your.email@odeal.com")
        print("   API_TOKEN: your-token")
        print("\n📝 Current config:")
        for key in ['JIRA_SERVER', 'PROJECT_KEY', 'EMAIL']:
            print(f"   {key}: {config.get(key, 'NOT SET')}")
        return

    # Get project
    try:
        project = jira.project(project_key)
        print(f"📊 Project: {project.name} ({project.key})")
        print(f"   Lead: {project.lead.displayName if hasattr(project, 'lead') else 'N/A'}")
        print()
    except Exception as e:
        print(f"⚠️  Could not fetch project details: {e}")
        print()

    # JQL query for team's work in 2025
    jql = f'''
        project = {project_key}
        AND created >= "{start_date}"
        AND created <= "{end_date}"
        ORDER BY created DESC
    '''

    print(f"🔎 Fetching issues...")
    print(f"   JQL: {jql}")
    print()

    # Fetch all issues
    try:
        issues = jira.search_issues(jql, maxResults=False, expand='changelog')
        print(f"✅ Found {len(issues)} issues in {project_key} for 2025\n")
    except Exception as e:
        print(f"❌ Error fetching issues: {e}")
        return

    if len(issues) == 0:
        print("⚠️  No issues found for this period")
        return

    # Analyze issues
    issue_data = []

    print("📊 Analyzing issues...")
    for i, issue in enumerate(issues, 1):
        print(f"[{i}/{len(issues)}] Processing {issue.key}...", end='\r')

        try:
            # Basic info
            data = {
                'key': issue.key,
                'summary': issue.fields.summary,
                'issue_type': issue.fields.issuetype.name,
                'status': issue.fields.status.name,
                'created': issue.fields.created,
                'updated': issue.fields.updated,
                'resolved': getattr(issue.fields, 'resolutiondate', None),
                'assignee': issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned',
                'assignee_key': issue.fields.assignee.name if issue.fields.assignee else None,
                'reporter': issue.fields.reporter.displayName if issue.fields.reporter else 'Unknown',
                'priority': issue.fields.priority.name if issue.fields.priority else 'None',
                'resolution': issue.fields.resolution.name if issue.fields.resolution else 'Unresolved',
            }

            # Story points (custom field - may vary)
            # Common field names: customfield_10016, customfield_10026
            story_points = None
            for field_name in dir(issue.fields):
                if 'customfield' in field_name:
                    try:
                        field_value = getattr(issue.fields, field_name)
                        # Check if it looks like story points (number between 0-100)
                        if isinstance(field_value, (int, float)) and 0 < field_value <= 100:
                            story_points = field_value
                            break
                    except:
                        pass

            data['story_points'] = story_points

            # Sprint info (if available)
            try:
                if hasattr(issue.fields, 'sprint'):
                    data['sprint'] = issue.fields.sprint.name if issue.fields.sprint else None
                else:
                    data['sprint'] = None
            except:
                data['sprint'] = None

            # Labels
            data['labels'] = ','.join(issue.fields.labels) if issue.fields.labels else ''

            # Components
            data['components'] = ','.join([c.name for c in issue.fields.components]) if issue.fields.components else ''

            issue_data.append(data)

        except Exception as e:
            print(f"\n⚠️  Error processing {issue.key}: {e}")
            continue

    print("\n")

    # Create DataFrame
    df = pd.DataFrame(issue_data)

    # Convert dates
    df['created'] = pd.to_datetime(df['created'])
    df['updated'] = pd.to_datetime(df['updated'])
    df['resolved'] = pd.to_datetime(df['resolved'])

    # Add month for analysis
    df['created_month'] = df['created'].dt.to_period('M')

    # Calculate resolution time for resolved issues
    df['resolution_days'] = (df['resolved'] - df['created']).dt.total_seconds() / 86400

    # ===============================
    # ANALYSIS
    # ===============================

    print("="*100)
    print("📊 TEAM PERFORMANCE ANALYSIS (2025)")
    print("="*100)
    print()

    total_issues = len(df)
    resolved_issues = len(df[df['resolved'].notna()])
    in_progress = len(df[df['status'].isin(['In Progress', 'In Review', 'In Development'])])
    done = len(df[df['status'].isin(['Done', 'Closed', 'Resolved'])])

    completion_rate = (done / total_issues * 100) if total_issues > 0 else 0

    print(f"📈 OVERALL METRICS:")
    print(f"   • Total Issues Created:    {total_issues}")
    print(f"   • Completed (Done):        {done} ({completion_rate:.1f}%)")
    print(f"   • In Progress:             {in_progress}")
    print(f"   • Resolution Rate:         {resolved_issues} ({resolved_issues/total_issues*100:.1f}%)")
    print()

    # Issue type breakdown
    print("┌" + "─" * 98 + "┐")
    print("│" + " " * 30 + "📋 ISSUE TYPE DISTRIBUTION" + " " * 42 + "│")
    print("├" + "─" * 98 + "┤")

    type_dist = df['issue_type'].value_counts()
    for itype, count in type_dist.items():
        percentage = (count / total_issues) * 100
        bar = "█" * int(percentage / 3)
        print(f"│ {itype:20s}: {count:>4} ({percentage:>5.1f}%)  {bar:30s}  │")

    print("└" + "─" * 98 + "┘")
    print()

    # Story Points
    if df['story_points'].notna().sum() > 0:
        total_sp = df['story_points'].sum()
        completed_sp = df[df['status'].isin(['Done', 'Closed', 'Resolved'])]['story_points'].sum()

        print(f"📊 STORY POINTS:")
        print(f"   • Total SP Created:        {total_sp:.0f}")
        print(f"   • Completed SP:            {completed_sp:.0f} ({completed_sp/total_sp*100:.1f}%)")
        print(f"   • Average SP per Issue:    {df['story_points'].mean():.1f}")
        print()
    else:
        print("⚠️  Story Points not tracked or not found in custom fields\n")

    # Monthly breakdown
    print("📅 MONTHLY ACTIVITY:")
    print()
    monthly = df.groupby('created_month').agg({
        'key': 'count',
        'story_points': 'sum'
    }).rename(columns={'key': 'issues'})

    print(monthly.to_string())
    print()

    # Status distribution
    print("┌" + "─" * 98 + "┐")
    print("│" + " " * 35 + "📊 STATUS DISTRIBUTION" + " " * 42 + "│")
    print("├" + "─" * 98 + "┤")

    status_dist = df['status'].value_counts()
    for status, count in status_dist.items():
        percentage = (count / total_issues) * 100
        print(f"│ {status:25s}: {count:>4} ({percentage:>5.1f}%)                                         │")

    print("└" + "─" * 98 + "┘")
    print()

    # Resolution time analysis
    resolved_df = df[df['resolution_days'].notna()]
    if len(resolved_df) > 0:
        print(f"⏱️  RESOLUTION TIME (for {len(resolved_df)} resolved issues):")
        print(f"   • Average:  {resolved_df['resolution_days'].mean():.1f} days")
        print(f"   • Median:   {resolved_df['resolution_days'].median():.1f} days")
        print(f"   • Min:      {resolved_df['resolution_days'].min():.1f} days")
        print(f"   • Max:      {resolved_df['resolution_days'].max():.1f} days")
        print()

    # Team member distribution
    print("👥 TEAM MEMBER ACTIVITY:")
    print()
    assignee_dist = df.groupby('assignee').agg({
        'key': 'count',
        'story_points': 'sum'
    }).rename(columns={'key': 'issues'}).sort_values('issues', ascending=False)

    print(assignee_dist.to_string())
    print()

    # Save to files
    output_dir = 'jira-analysis'
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Excel export
    excel_file = f'{output_dir}/jira_team_analysis_{project_key}_{timestamp}.xlsx'
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        # Summary
        summary = pd.DataFrame([
            {'Metric': 'Total Issues', 'Value': total_issues},
            {'Metric': 'Completed', 'Value': done},
            {'Metric': 'Completion Rate %', 'Value': f'{completion_rate:.1f}'},
            {'Metric': 'In Progress', 'Value': in_progress},
            {'Metric': 'Total SP', 'Value': total_sp if df['story_points'].notna().sum() > 0 else 'N/A'},
            {'Metric': 'Completed SP', 'Value': completed_sp if df['story_points'].notna().sum() > 0 else 'N/A'},
        ])
        summary.to_excel(writer, sheet_name='Summary', index=False)

        # All issues
        df.to_excel(writer, sheet_name='All Issues', index=False)

        # Monthly breakdown
        monthly.to_excel(writer, sheet_name='Monthly Breakdown')

        # Team member stats
        assignee_dist.to_excel(writer, sheet_name='Team Members')

        # Issue type breakdown
        type_dist.to_frame('count').to_excel(writer, sheet_name='Issue Types')

        # Status breakdown
        status_dist.to_frame('count').to_excel(writer, sheet_name='Status Distribution')

    print(f"📁 Detailed report saved: {excel_file}")

    # CSV export
    csv_file = f'{output_dir}/jira_issues_{project_key}_{timestamp}.csv'
    df.to_csv(csv_file, index=False)
    print(f"📁 CSV saved: {csv_file}")

    print()
    print("="*100)
    print("✅ Jira analysis complete!")
    print("="*100)

    return df


def main():
    # Parse env file
    config = parse_jira_env('jira.env')

    if 'API_TOKEN' not in config:
        print("❌ API_TOKEN not found in jira.env")
        sys.exit(1)

    if 'JIRA_SERVER' not in config:
        print("❌ Could not extract Jira server from jira.env")
        sys.exit(1)

    if 'PROJECT_KEY' not in config:
        print("❌ Could not extract project key from jira.env")
        sys.exit(1)

    # Run analysis
    analyze_jira_team(
        api_token=config['API_TOKEN'],
        jira_server=config['JIRA_SERVER'],
        project_key=config['PROJECT_KEY'],
        start_date='2025-01-01',
        end_date='2025-12-31',
        config=config
    )


if __name__ == "__main__":
    main()
