#!/usr/bin/env python3
"""
Jira Team Analysis using REST API directly
"""

import os
import sys
import requests
from datetime import datetime
import pandas as pd
import re
import json


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
        match = re.match(r'(https://[^/]+)', link)
        if match:
            config['JIRA_SERVER'] = match.group(1)

        if '/projects/' in link:
            project = link.split('/projects/')[1].split('/')[0]
            config['PROJECT_KEY'] = project

    return config


def fetch_jira_issues(email, api_token, jira_server, project_key, start_date, end_date):
    """Fetch issues using REST API v3"""

    print(f"\n{'='*100}")
    print(f"🎯 JIRA TEAM ANALYSIS: {project_key}")
    print(f"📅 Period: {start_date} to {end_date}")
    print(f"🔗 Server: {jira_server}")
    print(f"{'='*100}\n")

    # REST API v3 endpoint (new: /search/jql instead of /search)
    url = f"{jira_server}/rest/api/3/search/jql"

    # JQL query
    jql = f'project = {project_key} AND created >= "{start_date}" AND created <= "{end_date}" ORDER BY created DESC'

    print(f"🔎 Fetching issues from Jira...")
    print(f"   JQL: {jql}")
    print()

    # Fetch with pagination
    auth = (email, api_token)
    all_issues = []
    start_at = 0
    max_results = 100

    while True:
        params = {
            'jql': jql,
            'startAt': start_at,
            'maxResults': max_results,
            'fields': 'summary,issuetype,status,created,updated,resolutiondate,assignee,reporter,priority,resolution,labels,components,customfield_10016,customfield_10026'
        }

        try:
            response = requests.get(url, auth=auth, params=params)
            response.raise_for_status()

            data = response.json()
            issues = data.get('issues', [])
            total = data.get('total', 0)

            if not issues:
                break

            all_issues.extend(issues)
            print(f"   Fetched {len(all_issues)}/{total} issues...", end='\r')

            if len(all_issues) >= total:
                break

            start_at += max_results

        except Exception as e:
            print(f"\n❌ Error during pagination: {e}")
            break

    print(f"\n✅ Found {len(all_issues)} total issues")
    print()

    return all_issues

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"   Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def analyze_issues(issues, project_key):
    """Analyze fetched issues"""

    if not issues:
        print("⚠️  No issues to analyze")
        return

    print("="*100)
    print(f"📊 ANALYZING {len(issues)} ISSUES")
    print("="*100)
    print()

    # Extract data
    issue_data = []

    for issue in issues:
        fields = issue['fields']

        # Story points - check common custom fields
        story_points = None
        for field in ['customfield_10016', 'customfield_10026']:
            if field in fields and fields[field]:
                try:
                    sp = float(fields[field])
                    if 0 < sp <= 100:
                        story_points = sp
                        break
                except:
                    pass

        data = {
            'key': issue['key'],
            'summary': fields.get('summary', ''),
            'issue_type': fields['issuetype']['name'] if 'issuetype' in fields else 'Unknown',
            'status': fields['status']['name'] if 'status' in fields else 'Unknown',
            'created': fields.get('created'),
            'updated': fields.get('updated'),
            'resolved': fields.get('resolutiondate'),
            'assignee': fields['assignee']['displayName'] if fields.get('assignee') else 'Unassigned',
            'reporter': fields['reporter']['displayName'] if fields.get('reporter') else 'Unknown',
            'priority': fields['priority']['name'] if fields.get('priority') else 'None',
            'resolution': fields['resolution']['name'] if fields.get('resolution') else 'Unresolved',
            'story_points': story_points,
            'labels': ','.join(fields.get('labels', [])),
            'components': ','.join([c['name'] for c in fields.get('components', [])])
        }

        issue_data.append(data)

    # Create DataFrame
    df = pd.DataFrame(issue_data)

    # Convert dates (remove timezone for Excel compatibility)
    df['created'] = pd.to_datetime(df['created']).dt.tz_localize(None)
    df['updated'] = pd.to_datetime(df['updated']).dt.tz_localize(None)
    df['resolved'] = pd.to_datetime(df['resolved']).dt.tz_localize(None)

    df['created_month'] = df['created'].dt.to_period('M')
    df['resolution_days'] = (df['resolved'] - df['created']).dt.total_seconds() / 86400

    # Analysis
    total_issues = len(df)
    completed_statuses = ['Done', 'Closed', 'Resolved', 'Complete']
    done = len(df[df['status'].isin(completed_statuses)])
    in_progress_statuses = ['In Progress', 'In Review', 'In Development', 'To Do', 'Open']
    in_progress = len(df[df['status'].isin(in_progress_statuses)])

    completion_rate = (done / total_issues * 100) if total_issues > 0 else 0

    print(f"📈 OVERALL METRICS:")
    print(f"   • Total Issues Created:    {total_issues}")
    print(f"   • Completed:               {done} ({completion_rate:.1f}%)")
    print(f"   • In Progress:             {in_progress}")
    print()

    # Issue types
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
    has_sp = df['story_points'].notna().sum() > 0
    if has_sp:
        total_sp = df['story_points'].sum()
        completed_sp = df[df['status'].isin(completed_statuses)]['story_points'].sum()

        print(f"📊 STORY POINTS:")
        print(f"   • Total SP Created:        {total_sp:.0f} SP")
        print(f"   • Completed SP:            {completed_sp:.0f} SP ({completed_sp/total_sp*100:.1f}%)")
        print(f"   • Average SP per Issue:    {df[df['story_points'].notna()]['story_points'].mean():.1f} SP")
        print(f"   • Monthly Average:         {total_sp/12:.1f} SP/month")
        print()
    else:
        print("⚠️  Story Points not found in custom fields\n")

    # Monthly breakdown
    print("📅 MONTHLY ACTIVITY:")
    print()
    monthly = df.groupby('created_month').agg({
        'key': 'count',
        'story_points': 'sum'
    }).rename(columns={'key': 'issues'})

    for month in monthly.index:
        issues_count = monthly.loc[month, 'issues']
        sp = monthly.loc[month, 'story_points']
        bar = "█" * int(issues_count / 5)
        sp_str = f"{sp:.0f} SP" if pd.notna(sp) else "N/A"
        print(f"   {str(month):7s}  {bar:20s} {issues_count:>3} issues  ({sp_str:>6})")
    print()

    # Status distribution
    print("┌" + "─" * 98 + "┐")
    print("│" + " " * 35 + "📊 STATUS DISTRIBUTION" + " " * 42 + "│")
    print("├" + "─" * 98 + "┤")

    status_dist = df['status'].value_counts()
    for status, count in status_dist.items():
        percentage = (count / total_issues) * 100
        emoji = "✅" if status in completed_statuses else "⏳" if status in in_progress_statuses else "📝"
        print(f"│ {emoji} {status:23s}: {count:>4} ({percentage:>5.1f}%)                                         │")

    print("└" + "─" * 98 + "┘")
    print()

    # Team members
    print("👥 TEAM MEMBER ACTIVITY:")
    print()
    assignee_dist = df[df['assignee'] != 'Unassigned'].groupby('assignee').agg({
        'key': 'count',
        'story_points': 'sum'
    }).rename(columns={'key': 'issues'}).sort_values('issues', ascending=False)

    for person, row in assignee_dist.iterrows():
        sp_str = f"{row['story_points']:.0f} SP" if pd.notna(row['story_points']) else "N/A"
        print(f"   • {person:25s}: {row['issues']:>3} issues  ({sp_str:>8})")
    print()

    # Save outputs
    output_dir = 'jira-analysis'
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Excel
    excel_file = f'{output_dir}/jira_team_analysis_{project_key}_{timestamp}.xlsx'
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        summary = pd.DataFrame([
            {'Metric': 'Total Issues', 'Value': total_issues},
            {'Metric': 'Completed', 'Value': done},
            {'Metric': 'Completion Rate %', 'Value': f'{completion_rate:.1f}'},
            {'Metric': 'In Progress', 'Value': in_progress},
            {'Metric': 'Total SP', 'Value': total_sp if has_sp else 'N/A'},
            {'Metric': 'Completed SP', 'Value': completed_sp if has_sp else 'N/A'},
        ])
        summary.to_excel(writer, sheet_name='Summary', index=False)
        df.to_excel(writer, sheet_name='All Issues', index=False)
        monthly.to_excel(writer, sheet_name='Monthly Breakdown')
        assignee_dist.to_excel(writer, sheet_name='Team Members')
        type_dist.to_frame('count').to_excel(writer, sheet_name='Issue Types')
        status_dist.to_frame('count').to_excel(writer, sheet_name='Status')

    print(f"📁 Excel saved: {excel_file}")

    # CSV
    csv_file = f'{output_dir}/jira_issues_{project_key}_{timestamp}.csv'
    df.to_csv(csv_file, index=False)
    print(f"📁 CSV saved: {csv_file}")

    print()
    print("="*100)
    print("✅ Jira analysis complete!")
    print("="*100)

    return df


def main():
    config = parse_jira_env('jira.env')

    required = ['EMAIL', 'API_TOKEN', 'JIRA_SERVER', 'PROJECT_KEY']
    for req in required:
        if req not in config:
            print(f"❌ {req} not found in jira.env")
            sys.exit(1)

    issues = fetch_jira_issues(
        email=config['EMAIL'],
        api_token=config['API_TOKEN'],
        jira_server=config['JIRA_SERVER'],
        project_key=config['PROJECT_KEY'],
        start_date='2025-01-01',
        end_date='2025-12-31'
    )

    if issues:
        analyze_issues(issues, config['PROJECT_KEY'])


if __name__ == "__main__":
    main()
