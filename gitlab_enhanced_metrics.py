#!/usr/bin/env python3
"""
GitLab Enhanced Metrics - Quick Wins Implementation
Includes:
1. Temporal Patterns (hour/day analysis)
2. Code Quality from Commits
3. Rollback/Fix Tracking
4. Merge Conflict Detection
5. Productivity Metrics
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd
import re
from collections import defaultdict
from gitlab_dora_metrics import GitLabDORAMetrics


class GitLabEnhancedMetrics(GitLabDORAMetrics):
    """Enhanced metrics on top of base DORA metrics"""

    def __init__(self, gitlab_url: str, token: str):
        super().__init__(gitlab_url, token)

    def analyze_temporal_patterns(self, commits_df: pd.DataFrame) -> dict:
        """
        Analyze when people work (hour of day, day of week)

        Returns detailed temporal analysis
        """
        if commits_df.empty:
            return {}

        # Ensure datetime
        commits_df['committed_date'] = pd.to_datetime(commits_df['committed_date'])

        # Extract temporal features
        commits_df['hour'] = commits_df['committed_date'].dt.hour
        commits_df['day_of_week'] = commits_df['committed_date'].dt.dayofweek  # 0=Monday
        commits_df['is_weekend'] = commits_df['day_of_week'].isin([5, 6])
        commits_df['is_off_hours'] = (commits_df['hour'] < 8) | (commits_df['hour'] >= 20)

        analysis = {
            'hourly_distribution': commits_df['hour'].value_counts().sort_index().to_dict(),
            'daily_distribution': commits_df['day_of_week'].value_counts().sort_index().to_dict(),
            'weekend_commits': int(commits_df['is_weekend'].sum()),
            'weekend_percentage': round((commits_df['is_weekend'].sum() / len(commits_df)) * 100, 1),
            'off_hours_commits': int(commits_df['is_off_hours'].sum()),
            'off_hours_percentage': round((commits_df['is_off_hours'].sum() / len(commits_df)) * 100, 1),
        }

        # Peak hours
        hourly = commits_df['hour'].value_counts()
        analysis['peak_hour'] = int(hourly.idxmax())
        analysis['peak_hour_count'] = int(hourly.max())

        # Most productive day
        daily = commits_df['day_of_week'].value_counts()
        analysis['most_productive_day'] = int(daily.idxmax())
        analysis['most_productive_day_count'] = int(daily.max())

        return analysis

    def analyze_code_quality_from_commits(self, project_id: int, start_date: str, end_date: str) -> dict:
        """
        Analyze code quality indicators from commits:
        - Commit message quality
        - Change size (lines, files)
        - Fix/bug ratio
        - Code churn (same file changes)
        """
        try:
            proj = self.gl.projects.get(project_id)
            commits = proj.commits.list(since=start_date, until=end_date, all=True)

            commit_data = []
            fix_keywords = ['fix', 'hotfix', 'bugfix', 'patch', 'revert', 'rollback']

            for commit in commits:
                message = commit.message.lower()
                title = commit.title.lower()

                # Detect fix commits
                is_fix = any(keyword in message or keyword in title for keyword in fix_keywords)

                # Get commit details for change size
                try:
                    commit_detail = proj.commits.get(commit.id)
                    stats = commit_detail.stats
                    additions = stats.get('additions', 0)
                    deletions = stats.get('deletions', 0)
                    total_changes = additions + deletions
                except:
                    total_changes = 0
                    additions = 0
                    deletions = 0

                commit_data.append({
                    'sha': commit.id,
                    'title': commit.title,
                    'message': commit.message,
                    'message_length': len(commit.message),
                    'committed_date': commit.committed_date,
                    'is_fix': is_fix,
                    'additions': additions,
                    'deletions': deletions,
                    'total_changes': total_changes,
                    'author_name': commit.author_name,
                    'author_email': commit.author_email,
                })

            if not commit_data:
                return {}

            df = pd.DataFrame(commit_data)

            analysis = {
                'total_commits': len(df),
                'fix_commits': int(df['is_fix'].sum()),
                'fix_ratio': round((df['is_fix'].sum() / len(df)) * 100, 1),
                'avg_message_length': round(df['message_length'].mean(), 1),
                'avg_changes_per_commit': round(df['total_changes'].mean(), 1),
                'median_changes_per_commit': round(df['total_changes'].median(), 1),
                'large_commits': int((df['total_changes'] > 500).sum()),  # >500 lines
                'large_commits_percentage': round(((df['total_changes'] > 500).sum() / len(df)) * 100, 1),
            }

            # Commit message quality (longer = more descriptive, generally)
            short_messages = (df['message_length'] < 20).sum()
            analysis['short_message_commits'] = int(short_messages)
            analysis['short_message_percentage'] = round((short_messages / len(df)) * 100, 1)

            return analysis

        except Exception as e:
            print(f"Error analyzing code quality for project {project_id}: {e}")
            return {}

    def detect_merge_conflicts(self, project_id: int, start_date: str, end_date: str) -> dict:
        """
        Detect merge conflicts from MR notes/discussions
        """
        try:
            proj = self.gl.projects.get(project_id)
            mrs = proj.mergerequests.list(
                state='all',
                updated_after=start_date,
                updated_before=end_date,
                all=True
            )

            conflict_data = []
            conflict_keywords = ['conflict', 'merge conflict', 'conflicting', 'rebase']

            for mr in mrs:
                try:
                    # Check MR description and notes
                    has_conflict = False
                    conflict_mentions = 0

                    # Check description
                    if mr.description and any(kw in mr.description.lower() for kw in conflict_keywords):
                        has_conflict = True
                        conflict_mentions += 1

                    # Check notes
                    notes = mr.notes.list(all=True)
                    for note in notes:
                        if any(kw in note.body.lower() for kw in conflict_keywords):
                            has_conflict = True
                            conflict_mentions += 1

                    if has_conflict:
                        conflict_data.append({
                            'mr_iid': mr.iid,
                            'title': mr.title,
                            'author': mr.author['username'],
                            'conflict_mentions': conflict_mentions,
                            'created_at': mr.created_at,
                            'merged_at': mr.merged_at if hasattr(mr, 'merged_at') else None,
                        })

                except:
                    continue

            if not conflict_data:
                return {'total_mrs': len(mrs), 'conflict_count': 0, 'conflict_rate': 0.0}

            return {
                'total_mrs': len(mrs),
                'conflict_count': len(conflict_data),
                'conflict_rate': round((len(conflict_data) / len(mrs)) * 100, 1),
                'conflicts': conflict_data[:5]  # Top 5
            }

        except Exception as e:
            print(f"Error detecting conflicts for project {project_id}: {e}")
            return {}

    def analyze_pipeline_metrics(self, project_id: int, start_date: str, end_date: str) -> dict:
        """
        Analyze CI/CD pipeline performance
        """
        try:
            proj = self.gl.projects.get(project_id)

            # Get pipelines
            pipelines = proj.pipelines.list(
                updated_after=start_date,
                updated_before=end_date,
                all=True
            )

            if not pipelines:
                return {}

            success_count = 0
            failed_count = 0
            durations = []
            retry_success = 0  # Flaky detection

            pipeline_data = []

            for pipeline in pipelines:
                try:
                    # Get detailed pipeline
                    p_detail = proj.pipelines.get(pipeline.id)

                    status = p_detail.status
                    duration = p_detail.duration if p_detail.duration else 0

                    # Track status
                    if status == 'success':
                        success_count += 1
                        if duration:
                            durations.append(duration)
                    elif status == 'failed':
                        failed_count += 1

                    pipeline_data.append({
                        'id': pipeline.id,
                        'status': status,
                        'duration': duration,
                        'created_at': pipeline.created_at,
                        'ref': pipeline.ref,
                    })

                except:
                    continue

            total = success_count + failed_count
            if total == 0:
                return {}

            analysis = {
                'total_pipelines': total,
                'successful_pipelines': success_count,
                'failed_pipelines': failed_count,
                'success_rate': round((success_count / total) * 100, 1),
                'avg_duration_seconds': round(sum(durations) / len(durations), 1) if durations else 0,
                'avg_duration_minutes': round((sum(durations) / len(durations)) / 60, 1) if durations else 0,
            }

            return analysis

        except Exception as e:
            print(f"Error analyzing pipelines for project {project_id}: {e}")
            return {}

    def analyze_code_churn(self, project_id: int, start_date: str, end_date: str) -> dict:
        """
        Analyze code churn: how often the same files are modified
        High churn may indicate:
        1. Active development (good)
        2. Unstable code (bad)
        3. Frequent bug fixes (bad)
        """
        try:
            proj = self.gl.projects.get(project_id)
            commits = proj.commits.list(since=start_date, until=end_date, all=True)

            file_changes = defaultdict(int)
            commit_files = []

            for commit in commits[:100]:  # Limit for performance
                try:
                    c_detail = proj.commits.get(commit.id)
                    diffs = c_detail.diff()

                    for diff in diffs:
                        file_path = diff.get('new_path') or diff.get('old_path')
                        if file_path:
                            file_changes[file_path] += 1
                            commit_files.append({
                                'file': file_path,
                                'commit': commit.short_id,
                                'date': commit.committed_date,
                            })
                except:
                    continue

            if not file_changes:
                return {}

            # Get top churned files
            sorted_files = sorted(file_changes.items(), key=lambda x: x[1], reverse=True)
            top_churned = sorted_files[:10]

            analysis = {
                'total_unique_files': len(file_changes),
                'top_churned_files': [
                    {'file': f, 'change_count': c} for f, c in top_churned
                ],
                'high_churn_files': len([c for c in file_changes.values() if c >= 5]),  # Changed 5+ times
            }

            return analysis

        except Exception as e:
            print(f"Error analyzing code churn for project {project_id}: {e}")
            return {}


def generate_enhanced_report(username: str, group_id: int, start_date: str, end_date: str):
    """
    Generate comprehensive enhanced metrics report
    """
    load_dotenv()

    gitlab_url = os.getenv('GITLAB_URL')
    gitlab_token = os.getenv('GITLAB_TOKEN')

    if not gitlab_url or not gitlab_token:
        print("❌ Error: GITLAB_URL and GITLAB_TOKEN must be set")
        sys.exit(1)

    collector = GitLabEnhancedMetrics(gitlab_url, gitlab_token)

    print(f"\n{'='*80}")
    print(f"🔬 ENHANCED METRICS ANALYSIS: {username}")
    print(f"Date: {start_date} to {end_date}")
    print(f"{'='*80}\n")

    # Get projects
    projects = collector.get_group_projects(group_id)
    project_ids = [p['id'] for p in projects]

    print(f"Analyzing {len(project_ids)} projects...\n")

    # Collectors
    all_commits = []
    all_pipeline_metrics = []
    all_code_quality = []
    all_conflicts = []
    all_churn = []

    for i, proj_id in enumerate(project_ids, 1):
        print(f"[{i}/{len(project_ids)}] Analyzing project {proj_id}...", end='\r')

        try:
            proj = collector.gl.projects.get(proj_id)

            # Get commits
            commits = proj.commits.list(since=start_date, until=end_date, all=True)
            for c in commits:
                if username.lower() in c.author_name.lower() or username.lower() in c.author_email.lower():
                    all_commits.append({
                        'project': proj.name,
                        'sha': c.short_id,
                        'title': c.title,
                        'message': c.message,
                        'committed_date': c.committed_date,
                        'author_name': c.author_name,
                    })

            # Pipeline metrics (project-level)
            pipeline_metrics = collector.analyze_pipeline_metrics(proj_id, start_date, end_date)
            if pipeline_metrics:
                pipeline_metrics['project'] = proj.name
                all_pipeline_metrics.append(pipeline_metrics)

            # Code quality (project-level)
            quality = collector.analyze_code_quality_from_commits(proj_id, start_date, end_date)
            if quality:
                quality['project'] = proj.name
                all_code_quality.append(quality)

            # Conflicts
            conflicts = collector.detect_merge_conflicts(proj_id, start_date, end_date)
            if conflicts.get('conflict_count', 0) > 0:
                conflicts['project'] = proj.name
                all_conflicts.append(conflicts)

            # Code churn
            churn = collector.analyze_code_churn(proj_id, start_date, end_date)
            if churn:
                churn['project'] = proj.name
                all_churn.append(churn)

        except:
            continue

    # Generate reports
    print(f"\n\n{'='*80}")
    print("📊 ENHANCED METRICS SUMMARY")
    print(f"{'='*80}\n")

    # 1. TEMPORAL PATTERNS
    if all_commits:
        commits_df = pd.DataFrame(all_commits)
        temporal = collector.analyze_temporal_patterns(commits_df)

        print("⏰ TEMPORAL PATTERNS\n")
        print(f"Total Commits: {len(commits_df)}")
        print(f"Weekend Work: {temporal.get('weekend_percentage', 0)}% ({temporal.get('weekend_commits', 0)} commits)")
        print(f"Off-Hours Work: {temporal.get('off_hours_percentage', 0)}% ({temporal.get('off_hours_commits', 0)} commits)")
        print(f"\nPeak Hour: {temporal.get('peak_hour', 0):02d}:00 ({temporal.get('peak_hour_count', 0)} commits)")
        print(f"Most Productive Day: {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][temporal.get('most_productive_day', 0)]}")

    # 2. CODE QUALITY
    if all_code_quality:
        print(f"\n{'='*80}")
        print("💎 CODE QUALITY INDICATORS\n")

        for q in all_code_quality[:3]:  # Top 3 projects
            print(f"Project: {q['project']}")
            print(f"  Fix Ratio: {q.get('fix_ratio', 0)}%")
            print(f"  Avg Changes/Commit: {q.get('avg_changes_per_commit', 0)} lines")
            print(f"  Large Commits: {q.get('large_commits_percentage', 0)}%")
            print(f"  Short Messages: {q.get('short_message_percentage', 0)}%")
            print()

    # 3. PIPELINE HEALTH
    if all_pipeline_metrics:
        print(f"\n{'='*80}")
        print("🔧 CI/CD PIPELINE HEALTH\n")

        for p in all_pipeline_metrics[:3]:
            print(f"Project: {p['project']}")
            print(f"  Success Rate: {p.get('success_rate', 0)}%")
            print(f"  Avg Duration: {p.get('avg_duration_minutes', 0)} min")
            print(f"  Total Pipelines: {p.get('total_pipelines', 0)}")
            print()

    # 4. MERGE CONFLICTS
    if all_conflicts:
        print(f"\n{'='*80}")
        print("⚠️  MERGE CONFLICTS\n")

        total_conflicts = sum(c.get('conflict_count', 0) for c in all_conflicts)
        print(f"Total Projects with Conflicts: {len(all_conflicts)}")
        print(f"Total Conflicts Detected: {total_conflicts}")

    # 5. CODE CHURN
    if all_churn:
        print(f"\n{'='*80}")
        print("🔄 CODE CHURN ANALYSIS\n")

        for ch in all_churn[:2]:
            print(f"Project: {ch['project']}")
            print(f"  Unique Files Changed: {ch.get('total_unique_files', 0)}")
            print(f"  High Churn Files (5+ changes): {ch.get('high_churn_files', 0)}")
            print()

    print(f"\n{'='*80}")
    print("✅ Enhanced metrics analysis complete!")
    print(f"{'='*80}\n")


def main():
    load_dotenv()

    username = sys.argv[1] if len(sys.argv) > 1 else input("Enter username: ")
    group_id = int(os.getenv('GROUP_ID', 182))
    start_date = os.getenv('START_DATE', '2025-01-01')
    end_date = os.getenv('END_DATE', '2025-12-31')

    generate_enhanced_report(username, group_id, start_date, end_date)


if __name__ == '__main__':
    main()
