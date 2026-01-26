#!/usr/bin/env python3
"""
GitLab User Metrics Finder
Searches across all accessible projects to find a specific user's DORA metrics
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
from gitlab_dora_metrics import GitLabDORAMetrics


def find_user_metrics(gitlab_url: str, token: str, username: str, start_date: str, end_date: str):
    """
    Find metrics for a specific user across all accessible projects

    Args:
        gitlab_url: GitLab instance URL
        token: Personal access token
        username: Username to search for (can be partial, case-insensitive)
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """

    collector = GitLabDORAMetrics(gitlab_url, token)

    print(f"\n{'='*80}")
    print(f"Searching for user: {username}")
    print(f"Date range: {start_date} to {end_date}")
    print(f"{'='*80}\n")

    # Get all accessible groups
    try:
        groups = collector.gl.groups.list(all=True, order_by='name')
        print(f"Found {len(groups)} accessible groups\n")
    except Exception as e:
        print(f"Error fetching groups: {e}")
        groups = []

    # Get all accessible projects
    try:
        projects = collector.gl.projects.list(all=True, membership=True)
        print(f"Found {len(projects)} accessible projects\n")
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return

    all_user_mrs = []
    matching_projects = []

    # Search through all projects
    for i, project in enumerate(projects, 1):
        print(f"[{i}/{len(projects)}] Searching in {project.name}...", end='\r')

        try:
            # Get merge requests for this project
            mr_df = collector.get_merge_requests_by_user(
                project.id,
                start_date,
                end_date
            )

            if not mr_df.empty:
                # Filter by username (case-insensitive, partial match)
                user_df = mr_df[
                    mr_df['author'].str.contains(username, case=False, na=False) |
                    mr_df['author_name'].str.contains(username, case=False, na=False)
                ]

                if not user_df.empty:
                    user_df = collector.calculate_lead_time(user_df)
                    all_user_mrs.append(user_df)
                    matching_projects.append(project.name)
                    print(f"\n✓ Found {len(user_df)} MRs in {project.name}")

        except Exception as e:
            # Skip projects that error out
            continue

    print(f"\n\n{'='*80}")

    if not all_user_mrs:
        print(f"❌ No merge requests found for user matching '{username}'")
        print("\nPossible reasons:")
        print("1. Username is incorrect")
        print("2. User has no merged MRs in the date range")
        print("3. User's projects are not accessible with your token")
        return

    # Combine all MRs
    combined_mrs = pd.concat(all_user_mrs, ignore_index=True)

    print(f"✓ Found {len(combined_mrs)} total merge requests for '{username}'")
    print(f"  Across {len(matching_projects)} projects")
    print(f"{'='*80}\n")

    # Display project breakdown
    print("📦 Projects with contributions:")
    project_breakdown = combined_mrs.groupby('project_id').size().sort_values(ascending=False)
    for i, (proj_id, count) in enumerate(project_breakdown.items(), 1):
        proj_name = matching_projects[i-1] if i-1 < len(matching_projects) else f"Project {proj_id}"
        print(f"  {i}. {proj_name}: {count} MRs")

    # Calculate overall statistics
    print(f"\n{'='*80}")
    print(f"📊 Overall Statistics for '{username}'")
    print(f"{'='*80}\n")

    stats = {
        'Total Merge Requests': len(combined_mrs),
        'Average Lead Time (hours)': round(combined_mrs['lead_time_hours'].mean(), 2),
        'Median Lead Time (hours)': round(combined_mrs['lead_time_hours'].median(), 2),
        'Min Lead Time (hours)': round(combined_mrs['lead_time_hours'].min(), 2),
        'Max Lead Time (hours)': round(combined_mrs['lead_time_hours'].max(), 2),
        'Std Dev Lead Time (hours)': round(combined_mrs['lead_time_hours'].std(), 2),
    }

    for key, value in stats.items():
        print(f"{key:.<40} {value}")

    # Display recent MRs
    print(f"\n{'='*80}")
    print("🔄 Recent Merge Requests (last 10)")
    print(f"{'='*80}\n")

    recent_mrs = combined_mrs.nlargest(10, 'merged_at')[
        ['title', 'merged_at', 'lead_time_hours']
    ]
    print(recent_mrs.to_string(index=False))

    # Monthly breakdown
    print(f"\n{'='*80}")
    print("📅 Monthly Breakdown")
    print(f"{'='*80}\n")

    combined_mrs['month'] = pd.to_datetime(combined_mrs['merged_at']).dt.to_period('M')
    monthly_stats = combined_mrs.groupby('month').agg({
        'mr_id': 'count',
        'lead_time_hours': ['mean', 'median']
    }).round(2)
    monthly_stats.columns = ['MR Count', 'Avg Lead Time (h)', 'Median Lead Time (h)']
    print(monthly_stats.to_string())

    # Export results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_username = username.replace(' ', '_').replace('.', '_')
    output_dir = f"user-metrics-{safe_username}"

    os.makedirs(output_dir, exist_ok=True)

    # Export detailed MRs
    csv_file = f"{output_dir}/merge_requests_{safe_username}_{timestamp}.csv"
    combined_mrs.to_csv(csv_file, index=False)
    print(f"\n📁 Detailed MR data exported to {csv_file}")

    # Export summary statistics
    stats_df = pd.DataFrame([stats])
    stats_file = f"{output_dir}/summary_{safe_username}_{timestamp}.csv"
    stats_df.to_csv(stats_file, index=False)
    print(f"📁 Summary statistics exported to {stats_file}")

    # Export to Excel
    excel_file = f"{output_dir}/metrics_{safe_username}_{timestamp}.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        combined_mrs.to_excel(writer, sheet_name='All MRs', index=False)
        stats_df.to_excel(writer, sheet_name='Summary', index=False)
        monthly_stats.to_excel(writer, sheet_name='Monthly Breakdown')
    print(f"📁 Excel report exported to {excel_file}")

    print(f"\n{'='*80}")
    print("✅ User metrics collection complete!")
    print(f"{'='*80}\n")


def main():
    load_dotenv()

    gitlab_url = os.getenv('GITLAB_URL')
    gitlab_token = os.getenv('GITLAB_TOKEN')
    start_date = os.getenv('START_DATE', '2025-01-01')
    end_date = os.getenv('END_DATE', '2025-12-31')

    if not gitlab_url or not gitlab_token:
        print("❌ Error: GITLAB_URL and GITLAB_TOKEN must be set in .env file")
        sys.exit(1)

    # Get username from command line or prompt
    if len(sys.argv) > 1:
        username = ' '.join(sys.argv[1:])
    else:
        username = input("Enter username to search for (can be partial): ").strip()

    if not username:
        print("❌ Error: Username cannot be empty")
        sys.exit(1)

    find_user_metrics(gitlab_url, gitlab_token, username, start_date, end_date)


if __name__ == '__main__':
    main()
