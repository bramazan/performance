#!/usr/bin/env python3
"""
GitLab Direct Commits Metrics
Finds all commits by a user across projects, including direct commits to main/master
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
from gitlab_dora_metrics import GitLabDORAMetrics


def find_user_commits(gitlab_url: str, token: str, username: str, start_date: str, end_date: str):
    """
    Find all commits for a specific user across all accessible projects

    Args:
        gitlab_url: GitLab instance URL
        token: Personal access token
        username: Username to search for (can be partial, case-insensitive)
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """

    collector = GitLabDORAMetrics(gitlab_url, token)

    print(f"\n{'='*80}")
    print(f"Searching for commits by: {username}")
    print(f"Date range: {start_date} to {end_date}")
    print(f"{'='*80}\n")

    # Get all accessible projects
    try:
        projects = collector.gl.projects.list(all=True, membership=True)
        print(f"Found {len(projects)} accessible projects\n")
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return

    all_commits = []
    all_mr_commits = []
    matching_projects = []

    # Search through all projects
    for i, project in enumerate(projects, 1):
        print(f"[{i}/{len(projects)}] Searching in {project.name}...", end='\r')

        try:
            proj_obj = collector.gl.projects.get(project.id)

            # Get all commits in date range
            commits = proj_obj.commits.list(
                all=True,
                since=start_date,
                until=end_date
            )

            # Get merge requests to identify MR commits
            mr_list = proj_obj.mergerequests.list(
                state='merged',
                created_after=start_date,
                created_before=end_date,
                all=True
            )

            # Collect MR commit SHAs
            mr_commit_shas = set()
            for mr in mr_list:
                try:
                    mr_commits = mr.commits()
                    for c in mr_commits:
                        mr_commit_shas.add(c['id'])
                except:
                    pass

            user_commits = []
            user_mr_commits = []

            for commit in commits:
                # Check if commit author matches username
                author_name = commit.author_name.lower() if hasattr(commit, 'author_name') else ''
                author_email = commit.author_email.lower() if hasattr(commit, 'author_email') else ''
                committer_name = commit.committer_name.lower() if hasattr(commit, 'committer_name') else ''

                if (username.lower() in author_name or
                    username.lower() in author_email or
                    username.lower() in committer_name):

                    commit_data = {
                        'project_id': project.id,
                        'project_name': project.name,
                        'commit_sha': commit.id,
                        'short_sha': commit.short_id,
                        'title': commit.title,
                        'message': commit.message,
                        'author_name': commit.author_name,
                        'author_email': commit.author_email,
                        'committed_date': commit.committed_date,
                        'web_url': commit.web_url,
                        'is_merge_commit': len(commit.parent_ids) > 1,
                        'via_merge_request': commit.id in mr_commit_shas
                    }

                    if commit.id in mr_commit_shas:
                        user_mr_commits.append(commit_data)
                    else:
                        user_commits.append(commit_data)

            if user_commits or user_mr_commits:
                all_commits.extend(user_commits)
                all_mr_commits.extend(user_mr_commits)
                if project.name not in matching_projects:
                    matching_projects.append(project.name)
                print(f"\n✓ Found {len(user_commits)} direct commits + {len(user_mr_commits)} MR commits in {project.name}")

        except Exception as e:
            # Skip projects that error out
            continue

    print(f"\n\n{'='*80}")

    if not all_commits and not all_mr_commits:
        print(f"❌ No commits found for user matching '{username}'")
        return

    total_commits = len(all_commits) + len(all_mr_commits)
    print(f"✓ Found {total_commits} total commits for '{username}'")
    print(f"  • {len(all_commits)} direct commits (NOT via MR)")
    print(f"  • {len(all_mr_commits)} commits via Merge Request")
    print(f"  Across {len(matching_projects)} projects")
    print(f"{'='*80}\n")

    # Convert to dataframes
    if all_commits:
        direct_df = pd.DataFrame(all_commits)
        direct_df['committed_date'] = pd.to_datetime(direct_df['committed_date']).dt.tz_localize(None)
    else:
        direct_df = pd.DataFrame()

    if all_mr_commits:
        mr_df = pd.DataFrame(all_mr_commits)
        mr_df['committed_date'] = pd.to_datetime(mr_df['committed_date']).dt.tz_localize(None)
    else:
        mr_df = pd.DataFrame()

    all_df = pd.concat([direct_df, mr_df], ignore_index=True) if not direct_df.empty or not mr_df.empty else pd.DataFrame()

    if all_df.empty:
        return

    # Display project breakdown
    print("📦 Projects with commits:")
    project_breakdown = all_df.groupby('project_name').agg({
        'commit_sha': 'count',
        'via_merge_request': lambda x: sum(x)
    })
    project_breakdown.columns = ['Total Commits', 'Via MR']
    project_breakdown['Direct'] = project_breakdown['Total Commits'] - project_breakdown['Via MR']
    project_breakdown = project_breakdown.sort_values('Total Commits', ascending=False)

    for idx, (proj_name, row) in enumerate(project_breakdown.iterrows(), 1):
        print(f"  {idx}. {proj_name}: {int(row['Total Commits'])} commits ({int(row['Direct'])} direct, {int(row['Via MR'])} via MR)")

    # Calculate statistics
    print(f"\n{'='*80}")
    print(f"📊 Commit Statistics for '{username}'")
    print(f"{'='*80}\n")

    stats = {
        'Total Commits': len(all_df),
        'Direct Commits (No MR)': len(all_commits),
        'Commits via MR': len(all_mr_commits),
        'Projects Contributed': len(matching_projects),
        'Merge Commits': all_df['is_merge_commit'].sum(),
    }

    for key, value in stats.items():
        print(f"{key:.<40} {value}")

    # Display recent direct commits (most important!)
    if not direct_df.empty:
        print(f"\n{'='*80}")
        print("⚠️  DIRECT COMMITS (NOT via Merge Request)")
        print(f"{'='*80}\n")

        recent_direct = direct_df.nlargest(20, 'committed_date')[
            ['project_name', 'title', 'committed_date', 'short_sha']
        ]
        print(recent_direct.to_string(index=False))
    else:
        print(f"\n✅ No direct commits found - all commits were via Merge Requests (good practice!)")

    # Monthly breakdown
    print(f"\n{'='*80}")
    print("📅 Monthly Commit Breakdown")
    print(f"{'='*80}\n")

    all_df['month'] = pd.to_datetime(all_df['committed_date']).dt.to_period('M')

    # Create separate counts for direct and MR commits
    monthly_stats = all_df.groupby('month').agg({
        'commit_sha': 'count',
        'via_merge_request': lambda x: sum(x)
    })
    monthly_stats.columns = ['Total Commits', 'Via MR']
    monthly_stats['Direct Commits'] = monthly_stats['Total Commits'] - monthly_stats['Via MR']
    monthly_stats = monthly_stats[['Total Commits', 'Direct Commits', 'Via MR']]
    print(monthly_stats.to_string())

    # Export results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_username = username.replace(' ', '_').replace('.', '_')
    output_dir = f"user-commits-{safe_username}"

    os.makedirs(output_dir, exist_ok=True)

    # Export all commits
    if not all_df.empty:
        csv_file = f"{output_dir}/all_commits_{safe_username}_{timestamp}.csv"
        all_df.to_csv(csv_file, index=False)
        print(f"\n📁 All commits exported to {csv_file}")

    # Export direct commits separately
    if not direct_df.empty:
        direct_csv = f"{output_dir}/direct_commits_{safe_username}_{timestamp}.csv"
        direct_df.to_csv(direct_csv, index=False)
        print(f"📁 Direct commits exported to {direct_csv}")

    # Export to Excel
    excel_file = f"{output_dir}/commits_{safe_username}_{timestamp}.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        if not all_df.empty:
            all_df.to_excel(writer, sheet_name='All Commits', index=False)
        if not direct_df.empty:
            direct_df.to_excel(writer, sheet_name='Direct Commits', index=False)
        if not mr_df.empty:
            mr_df.to_excel(writer, sheet_name='MR Commits', index=False)
        monthly_stats.to_excel(writer, sheet_name='Monthly Breakdown')
        project_breakdown.to_excel(writer, sheet_name='By Project')
    print(f"📁 Excel report exported to {excel_file}")

    print(f"\n{'='*80}")
    print("✅ Commit analysis complete!")
    print(f"{'='*80}\n")


def main():
    load_dotenv()

    gitlab_url = os.getenv('GITLAB_URL')
    gitlab_token = os.getenv('GITLAB_TOKEN')
    start_date = os.getenv('START_DATE', '2024-01-01')
    end_date = os.getenv('END_DATE', '2024-12-31')

    if not gitlab_url or not gitlab_token:
        print("❌ Error: GITLAB_URL and GITLAB_TOKEN must be set in .env file")
        sys.exit(1)

    # Get username from command line or prompt
    if len(sys.argv) > 1:
        username = ' '.join(sys.argv[1:])
    else:
        username = input("Enter username to search for: ").strip()

    if not username:
        print("❌ Error: Username cannot be empty")
        sys.exit(1)

    find_user_commits(gitlab_url, gitlab_token, username, start_date, end_date)


if __name__ == '__main__':
    main()
