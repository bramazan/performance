#!/usr/bin/env python3
"""
GitLab Team Lead Analysis
Comprehensive analysis of a Team Lead's activities including:
- Code reviews (comments, approvals)
- Direct code contributions
- Issue management
- Team collaboration
- Leadership indicators
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
from gitlab_dora_metrics import GitLabDORAMetrics
from collections import defaultdict


def analyze_team_lead(gitlab_url: str, token: str, username: str, start_date: str, end_date: str, group_id: int = None):
    """
    Comprehensive Team Lead analysis

    Args:
        gitlab_url: GitLab instance URL
        token: Personal access token
        username: Username to analyze
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        group_id: Optional group ID to limit analysis
    """

    collector = GitLabDORAMetrics(gitlab_url, token)

    print(f"\n{'='*80}")
    print(f"🎯 TEAM LEAD ANALYSIS: {username}")
    print(f"Date range: {start_date} to {end_date}")
    print(f"{'='*80}\n")

    # Get projects to analyze
    if group_id:
        print(f"Analyzing group ID: {group_id}")
        projects = collector.get_group_projects(group_id)
        project_ids = [p['id'] for p in projects]
    else:
        projects = collector.gl.projects.list(all=True, membership=True)
        project_ids = [p.id for p in projects]

    print(f"Analyzing {len(project_ids)} projects...\n")

    # Data collectors
    commits_data = []
    mr_created_data = []
    mr_reviewed_data = []
    mr_approved_data = []
    mr_comments_data = []
    issues_created_data = []
    issues_assigned_data = []
    notes_data = []

    # Analyze each project
    for i, proj_id in enumerate(project_ids, 1):
        print(f"[{i}/{len(project_ids)}] Analyzing project {proj_id}...", end='\r')

        try:
            proj = collector.gl.projects.get(proj_id)
            proj_name = proj.name

            # 1. COMMITS - Direct code contributions
            try:
                commits = proj.commits.list(since=start_date, until=end_date, all=True)
                for commit in commits:
                    author_name = getattr(commit, 'author_name', '').lower()
                    author_email = getattr(commit, 'author_email', '').lower()

                    if username.lower() in author_name or username.lower() in author_email:
                        commits_data.append({
                            'project': proj_name,
                            'date': commit.committed_date,
                            'title': commit.title,
                            'sha': commit.short_id
                        })
            except:
                pass

            # 2. MERGE REQUESTS CREATED - Leading by example
            try:
                mrs_created = proj.mergerequests.list(
                    author_username=username,
                    created_after=start_date,
                    created_before=end_date,
                    all=True
                )
                for mr in mrs_created:
                    mr_created_data.append({
                        'project': proj_name,
                        'title': mr.title,
                        'state': mr.state,
                        'created_at': mr.created_at,
                        'merged_at': getattr(mr, 'merged_at', None),
                        'url': mr.web_url
                    })
            except:
                pass

            # 3. MERGE REQUESTS REVIEWED - Code review activity
            try:
                all_mrs = proj.mergerequests.list(
                    updated_after=start_date,
                    updated_before=end_date,
                    all=True
                )

                for mr in all_mrs:
                    try:
                        # Get detailed MR info
                        mr_detail = proj.mergerequests.get(mr.iid)

                        # Check approvals
                        try:
                            approvals = mr_detail.approvals.get()
                            for approver in approvals.approved_by:
                                if username.lower() in approver['user']['username'].lower():
                                    mr_approved_data.append({
                                        'project': proj_name,
                                        'mr_title': mr.title,
                                        'mr_author': mr.author['username'],
                                        'approved_at': mr.updated_at,
                                        'url': mr.web_url
                                    })
                        except:
                            pass

                        # Get comments/notes
                        try:
                            notes = mr_detail.notes.list(all=True)
                            for note in notes:
                                if username.lower() in note.author['username'].lower():
                                    mr_comments_data.append({
                                        'project': proj_name,
                                        'mr_title': mr.title,
                                        'mr_author': mr.author['username'],
                                        'comment': note.body[:200],  # First 200 chars
                                        'created_at': note.created_at,
                                        'url': mr.web_url
                                    })
                        except:
                            pass

                    except:
                        continue

            except:
                pass

            # 4. ISSUES - Project management
            try:
                # Issues created
                issues_created = proj.issues.list(
                    author_username=username,
                    created_after=start_date,
                    created_before=end_date,
                    all=True
                )
                for issue in issues_created:
                    issues_created_data.append({
                        'project': proj_name,
                        'title': issue.title,
                        'state': issue.state,
                        'created_at': issue.created_at,
                        'url': issue.web_url
                    })

                # Issues assigned to user
                issues_assigned = proj.issues.list(
                    assignee_username=username,
                    updated_after=start_date,
                    updated_before=end_date,
                    all=True
                )
                for issue in issues_assigned:
                    issues_assigned_data.append({
                        'project': proj_name,
                        'title': issue.title,
                        'state': issue.state,
                        'assigned_at': issue.updated_at
                    })

            except:
                pass

        except Exception as e:
            continue

    # Generate comprehensive report
    print(f"\n\n{'='*80}")
    print(f"📊 TEAM LEAD ACTIVITY SUMMARY")
    print(f"{'='*80}\n")

    summary_stats = {
        '💻 Code Contributions': {
            'Total Commits': len(commits_data),
            'MRs Created': len(mr_created_data),
        },
        '👀 Code Review Activity': {
            'MRs Approved': len(mr_approved_data),
            'MR Comments': len(mr_comments_data),
        },
        '📋 Project Management': {
            'Issues Created': len(issues_created_data),
            'Issues Assigned': len(issues_assigned_data),
        }
    }

    for category, metrics in summary_stats.items():
        print(f"\n{category}")
        print("-" * 40)
        for metric, value in metrics.items():
            print(f"  {metric:.<30} {value}")

    # Calculate review ratio
    total_activity = len(commits_data) + len(mr_created_data) + len(mr_approved_data) + len(mr_comments_data)
    if total_activity > 0:
        review_percentage = ((len(mr_approved_data) + len(mr_comments_data)) / total_activity) * 100
        print(f"\n{'='*80}")
        print(f"🎯 LEADERSHIP INDICATORS")
        print(f"{'='*80}")
        print(f"  Review Activity Ratio............. {review_percentage:.1f}%")
        print(f"  (Higher % = More time on reviews vs coding)")

    # Monthly breakdown
    if mr_comments_data or mr_approved_data:
        print(f"\n{'='*80}")
        print(f"📅 CODE REVIEW ACTIVITY BY MONTH")
        print(f"{'='*80}\n")

        # Combine all review activities
        all_reviews = []
        for item in mr_approved_data:
            all_reviews.append({'date': item['approved_at'], 'type': 'approval'})
        for item in mr_comments_data:
            all_reviews.append({'date': item['created_at'], 'type': 'comment'})

        if all_reviews:
            review_df = pd.DataFrame(all_reviews)
            review_df['date'] = pd.to_datetime(review_df['date']).dt.tz_localize(None)
            review_df['month'] = review_df['date'].dt.to_period('M')

            monthly_reviews = review_df.groupby(['month', 'type']).size().unstack(fill_value=0)
            monthly_reviews['Total'] = monthly_reviews.sum(axis=1)
            print(monthly_reviews.to_string())

    # Top reviewed MRs
    if mr_comments_data:
        print(f"\n{'='*80}")
        print(f"💬 RECENT CODE REVIEW COMMENTS (Last 10)")
        print(f"{'='*80}\n")

        comments_df = pd.DataFrame(mr_comments_data)
        comments_df['created_at'] = pd.to_datetime(comments_df['created_at']).dt.tz_localize(None)
        recent_comments = comments_df.nlargest(10, 'created_at')[
            ['project', 'mr_title', 'mr_author', 'comment', 'created_at']
        ]
        print(recent_comments.to_string(index=False))

    # Export detailed reports
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_username = username.replace(' ', '_').replace('.', '_')
    output_dir = f"team-lead-analysis-{safe_username}"

    os.makedirs(output_dir, exist_ok=True)

    # Export to Excel with multiple sheets
    excel_file = f"{output_dir}/team_lead_report_{safe_username}_{timestamp}.xlsx"

    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        # Summary sheet
        summary_data = []
        for category, metrics in summary_stats.items():
            for metric, value in metrics.items():
                summary_data.append({'Category': category, 'Metric': metric, 'Value': value})
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)

        # Individual activity sheets
        if commits_data:
            pd.DataFrame(commits_data).to_excel(writer, sheet_name='Commits', index=False)
        if mr_created_data:
            pd.DataFrame(mr_created_data).to_excel(writer, sheet_name='MRs Created', index=False)
        if mr_approved_data:
            pd.DataFrame(mr_approved_data).to_excel(writer, sheet_name='MRs Approved', index=False)
        if mr_comments_data:
            pd.DataFrame(mr_comments_data).to_excel(writer, sheet_name='MR Comments', index=False)
        if issues_created_data:
            pd.DataFrame(issues_created_data).to_excel(writer, sheet_name='Issues Created', index=False)

    print(f"\n📁 Detailed report exported to {excel_file}")

    # Create summary CSV
    summary_csv = f"{output_dir}/summary_{safe_username}_{timestamp}.csv"
    pd.DataFrame(summary_data).to_csv(summary_csv, index=False)
    print(f"📁 Summary exported to {summary_csv}")

    print(f"\n{'='*80}")
    print("✅ Team Lead analysis complete!")
    print(f"{'='*80}\n")

    # Final assessment
    print(f"{'='*80}")
    print(f"🎓 ASSESSMENT FOR TEAM LEAD ROLE")
    print(f"{'='*80}\n")

    total_reviews = len(mr_approved_data) + len(mr_comments_data)
    total_code = len(commits_data) + len(mr_created_data)

    print("Key Indicators:")
    print(f"  • Code Review Activity: {total_reviews} actions")
    print(f"  • Direct Code Contribution: {total_code} actions")

    if total_reviews > total_code:
        print(f"\n✅ STRONG TEAM LEAD PROFILE")
        print(f"   More focus on reviewing/mentoring ({total_reviews}) vs coding ({total_code})")
        print(f"   This is expected and healthy for a Team Lead role.")
    elif total_reviews > 0:
        print(f"\n⚠️  BALANCED PROFILE")
        print(f"   Mix of coding ({total_code}) and reviewing ({total_reviews})")
        print(f"   Consider increasing review activity for stronger leadership presence.")
    else:
        print(f"\n⚠️  CODE-HEAVY PROFILE")
        print(f"   Mostly coding ({total_code}) with limited review activity ({total_reviews})")
        print(f"   May need to delegate more coding and focus on team guidance.")

    print(f"\n{'='*80}\n")


def main():
    load_dotenv()

    gitlab_url = os.getenv('GITLAB_URL')
    gitlab_token = os.getenv('GITLAB_TOKEN')
    start_date = os.getenv('START_DATE', '2024-01-01')
    end_date = os.getenv('END_DATE', '2024-12-31')
    group_id = os.getenv('GROUP_ID')

    if not gitlab_url or not gitlab_token:
        print("❌ Error: GITLAB_URL and GITLAB_TOKEN must be set in .env file")
        sys.exit(1)

    # Get username from command line or prompt
    if len(sys.argv) > 1:
        username = ' '.join(sys.argv[1:])
    else:
        username = input("Enter username to analyze: ").strip()

    if not username:
        print("❌ Error: Username cannot be empty")
        sys.exit(1)

    analyze_team_lead(
        gitlab_url,
        gitlab_token,
        username,
        start_date,
        end_date,
        int(group_id) if group_id else None
    )


if __name__ == '__main__':
    main()
