#!/usr/bin/env python3
"""
GitLab DORA Metrics Collector
Collects DORA metrics (Deployment Frequency, Lead Time for Changes,
Time to Restore Service, Change Failure Rate) from GitLab for teams and individuals.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import requests
import pandas as pd
from dotenv import load_dotenv
import gitlab
import json


class GitLabDORAMetrics:
    """Fetches and processes DORA metrics from GitLab"""

    def __init__(self, gitlab_url: str, token: str):
        """
        Initialize GitLab connection

        Args:
            gitlab_url: GitLab instance URL
            token: Personal access token with api scope
        """
        self.gitlab_url = gitlab_url.rstrip('/')
        self.token = token
        self.gl = gitlab.Gitlab(gitlab_url, private_token=token)
        self.session = requests.Session()
        self.session.headers.update({
            'PRIVATE-TOKEN': token,
            'Content-Type': 'application/json'
        })

    def get_dora_metrics(
        self,
        project_id: int,
        metric: str,
        start_date: str,
        end_date: str,
        interval: str = 'daily'
    ) -> List[Dict[str, Any]]:
        """
        Fetch DORA metrics for a specific project

        Args:
            project_id: GitLab project ID
            metric: One of 'deployment_frequency', 'lead_time_for_changes',
                   'time_to_restore_service', 'change_failure_rate'
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            interval: Aggregation interval ('daily', 'monthly', 'all')

        Returns:
            List of metric data points
        """
        url = f"{self.gitlab_url}/api/v4/projects/{project_id}/dora/metrics"
        params = {
            'metric': metric,
            'start_date': start_date,
            'end_date': end_date,
            'interval': interval
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Warning: DORA metrics not available for project {project_id}")
                print("Note: DORA metrics require GitLab Ultimate license")
                return []
            else:
                raise

    def get_all_dora_metrics(
        self,
        project_id: int,
        start_date: str,
        end_date: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch all DORA metrics for a project

        Returns:
            Dictionary with all four DORA metrics
        """
        metrics = {
            'deployment_frequency': [],
            'lead_time_for_changes': [],
            'time_to_restore_service': [],
            'change_failure_rate': []
        }

        for metric_name in metrics.keys():
            print(f"Fetching {metric_name} for project {project_id}...")
            data = self.get_dora_metrics(
                project_id,
                metric_name,
                start_date,
                end_date
            )
            metrics[metric_name] = data

        return metrics

    def get_deployments(
        self,
        project_id: int,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Alternative: Fetch deployments directly from environments
        (Useful if DORA API is not available)
        """
        url = f"{self.gitlab_url}/api/v4/projects/{project_id}/deployments"
        params = {
            'updated_after': start_date,
            'updated_before': end_date,
            'per_page': 100
        }

        deployments = []
        page = 1

        while True:
            params['page'] = page
            response = self.session.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            if not data:
                break

            deployments.extend(data)
            page += 1

        return deployments

    def get_merge_requests_by_user(
        self,
        project_id: int,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """
        Get merge requests grouped by user (for individual metrics)
        """
        url = f"{self.gitlab_url}/api/v4/projects/{project_id}/merge_requests"
        params = {
            'state': 'merged',
            'created_after': start_date,
            'created_before': end_date,
            'per_page': 100
        }

        merge_requests = []
        page = 1

        print(f"Fetching merge requests for project {project_id}...")

        while True:
            params['page'] = page
            response = self.session.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            if not data:
                break

            for mr in data:
                merge_requests.append({
                    'project_id': project_id,
                    'mr_id': mr['iid'],
                    'title': mr['title'],
                    'author': mr['author']['username'],
                    'author_name': mr['author']['name'],
                    'created_at': mr['created_at'],
                    'merged_at': mr['merged_at'],
                    'web_url': mr['web_url']
                })

            page += 1

            if page > 10:  # Safety limit
                break

        return pd.DataFrame(merge_requests)

    def calculate_lead_time(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate lead time for changes from merge request data
        """
        if df.empty:
            return df

        # Convert to datetime and remove timezone info for Excel compatibility
        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_localize(None)
        df['merged_at'] = pd.to_datetime(df['merged_at']).dt.tz_localize(None)
        df['lead_time_hours'] = (
            df['merged_at'] - df['created_at']
        ).dt.total_seconds() / 3600

        return df

    def get_group_projects(self, group_id: int) -> List[Dict[str, Any]]:
        """
        Get all projects in a group (for team metrics)
        """
        try:
            group = self.gl.groups.get(group_id)
            projects = group.projects.list(all=True)
            return [{'id': p.id, 'name': p.name} for p in projects]
        except Exception as e:
            print(f"Error fetching group projects: {e}")
            return []

    def export_to_csv(self, data: pd.DataFrame, filename: str):
        """Export data to CSV"""
        data.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data exported to {filename}")

    def export_to_excel(self, data_dict: Dict[str, pd.DataFrame], filename: str):
        """Export multiple dataframes to Excel with separate sheets"""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Data exported to {filename}")


def main():
    """Main execution function"""

    # Load environment variables
    load_dotenv()

    gitlab_url = os.getenv('GITLAB_URL')
    gitlab_token = os.getenv('GITLAB_TOKEN')
    start_date = os.getenv('START_DATE', '2024-01-01')
    end_date = os.getenv('END_DATE', '2024-12-31')

    if not gitlab_url or not gitlab_token:
        print("Error: GITLAB_URL and GITLAB_TOKEN must be set in .env file")
        sys.exit(1)

    # Initialize collector
    collector = GitLabDORAMetrics(gitlab_url, gitlab_token)

    # Get project IDs from environment
    project_ids_str = os.getenv('PROJECT_IDS', '')
    group_id_str = os.getenv('GROUP_ID', '')

    project_ids = []

    if group_id_str:
        # Fetch projects from group
        print(f"Fetching projects from group {group_id_str}...")
        projects = collector.get_group_projects(int(group_id_str))
        project_ids = [p['id'] for p in projects]
        print(f"Found {len(project_ids)} projects in group")
    elif project_ids_str:
        # Use specified project IDs
        project_ids = [int(pid.strip()) for pid in project_ids_str.split(',')]
    else:
        print("Error: Either PROJECT_IDS or GROUP_ID must be set")
        sys.exit(1)

    # Collect metrics for all projects
    all_metrics = {}
    all_merge_requests = []

    for project_id in project_ids:
        print(f"\n{'='*60}")
        print(f"Processing project {project_id}")
        print(f"{'='*60}")

        # Try to get DORA metrics (requires GitLab Ultimate)
        try:
            metrics = collector.get_all_dora_metrics(
                project_id,
                start_date,
                end_date
            )
            all_metrics[project_id] = metrics
        except Exception as e:
            print(f"Could not fetch DORA metrics: {e}")
            print("Falling back to manual calculation from MR data...")

        # Get merge requests (works on all GitLab tiers)
        mr_df = collector.get_merge_requests_by_user(
            project_id,
            start_date,
            end_date
        )

        if not mr_df.empty:
            mr_df = collector.calculate_lead_time(mr_df)
            all_merge_requests.append(mr_df)

    # Combine all merge requests
    if all_merge_requests:
        combined_mrs = pd.concat(all_merge_requests, ignore_index=True)

        # Generate summary statistics by user
        user_stats = combined_mrs.groupby(['author', 'author_name']).agg({
            'mr_id': 'count',
            'lead_time_hours': ['mean', 'median', 'min', 'max']
        }).round(2)

        user_stats.columns = [
            'total_mrs',
            'avg_lead_time_hours',
            'median_lead_time_hours',
            'min_lead_time_hours',
            'max_lead_time_hours'
        ]
        user_stats = user_stats.reset_index()

        print(f"\n{'='*60}")
        print("Summary Statistics by User")
        print(f"{'='*60}")
        print(user_stats.to_string(index=False))

        # Export results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Export detailed MR data
        collector.export_to_csv(
            combined_mrs,
            f'gitlab_merge_requests_{timestamp}.csv'
        )

        # Export user statistics
        collector.export_to_csv(
            user_stats,
            f'gitlab_user_stats_{timestamp}.csv'
        )

        # Export to Excel with multiple sheets
        excel_data = {
            'Merge Requests': combined_mrs,
            'User Statistics': user_stats
        }

        collector.export_to_excel(
            excel_data,
            f'gitlab_dora_metrics_{timestamp}.xlsx'
        )

        # Save raw DORA metrics if available
        if all_metrics:
            with open(f'gitlab_dora_raw_{timestamp}.json', 'w') as f:
                json.dump(all_metrics, f, indent=2)
            print(f"Raw DORA metrics exported to gitlab_dora_raw_{timestamp}.json")

    print(f"\n{'='*60}")
    print("Collection complete!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
