#!/usr/bin/env python3
"""
Bug Ratio Analysis - Analyzes bug/fix ratio from GitLab MR data
"""

import pandas as pd
import os
import re
from pathlib import Path

def is_bug_or_fix(title):
    """
    Determine if an MR is a bug/fix based on title keywords
    """
    title_lower = title.lower()

    # Bug/fix indicators
    bug_keywords = [
        'fix', 'bug', 'hotfix', 'patch', 'resolve',
        'fixes', 'fixed', 'bugfix', 'defect',
        'null check', 'exception', 'error',
        'corrects', 'correction'
    ]

    # Feature indicators (to exclude false positives)
    feature_keywords = [
        'adds', 'add', 'new feature', 'implement',
        'enhancement', 'improvement', 'refactor',
        'update', 'upgrade'
    ]

    # Check for bug keywords
    has_bug_keyword = any(keyword in title_lower for keyword in bug_keywords)

    # If it has "adds" or similar, it's likely a feature, not a fix
    # Exception: "adds null check" or "adds fix" are still fixes
    has_feature_keyword = any(keyword in title_lower for keyword in feature_keywords)
    if has_feature_keyword and not any(word in title_lower for word in ['null check', 'checks', 'validation', 'control']):
        return False

    return has_bug_keyword

def analyze_user_bugs(csv_file):
    """
    Analyze bugs for a single user
    """
    df = pd.read_csv(csv_file)

    # Classify each MR
    df['is_bug'] = df['title'].apply(is_bug_or_fix)

    total_mrs = len(df)
    bug_mrs = df['is_bug'].sum()
    feature_mrs = total_mrs - bug_mrs
    bug_ratio = (bug_mrs / total_mrs * 100) if total_mrs > 0 else 0

    # Get sample bugs
    bug_titles = df[df['is_bug']]['title'].head(10).tolist()

    return {
        'total_mrs': total_mrs,
        'bug_mrs': bug_mrs,
        'feature_mrs': feature_mrs,
        'bug_ratio': bug_ratio,
        'sample_bugs': bug_titles
    }

def main():
    # Find all user metric directories
    base_dir = Path('.')
    user_dirs = [d for d in base_dir.glob('user-metrics-*') if d.is_dir()]

    results = []

    for user_dir in user_dirs:
        # Get the most recent CSV file
        csv_files = list(user_dir.glob('merge_requests_*.csv'))
        if not csv_files:
            continue

        # Get the most recent file
        latest_csv = max(csv_files, key=lambda x: x.stat().st_mtime)

        # Extract username
        username = user_dir.name.replace('user-metrics-', '')

        print(f"\nAnalyzing {username}...")

        try:
            analysis = analyze_user_bugs(latest_csv)
            analysis['username'] = username
            results.append(analysis)

            print(f"  Total MRs: {analysis['total_mrs']}")
            print(f"  Bug/Fix MRs: {analysis['bug_mrs']}")
            print(f"  Feature MRs: {analysis['feature_mrs']}")
            print(f"  Bug Ratio: {analysis['bug_ratio']:.1f}%")

        except Exception as e:
            print(f"  Error: {e}")

    # Sort by bug ratio
    results.sort(key=lambda x: x['bug_ratio'], reverse=True)

    print("\n" + "="*80)
    print("BUG RATIO COMPARISON - ALL DEVELOPERS")
    print("="*80 + "\n")

    print(f"{'Developer':<20} {'Total MRs':<12} {'Bug MRs':<12} {'Feature MRs':<12} {'Bug %':<10}")
    print("-" * 80)

    for r in results:
        print(f"{r['username']:<20} {r['total_mrs']:<12} {r['bug_mrs']:<12} {r['feature_mrs']:<12} {r['bug_ratio']:<10.1f}%")

    print("\n" + "="*80)
    print("DETAILED ANALYSIS")
    print("="*80)

    for r in results:
        print(f"\n{r['username'].upper()}")
        print("-" * 40)
        print(f"Bug Ratio: {r['bug_ratio']:.1f}%")
        print(f"\nSample Bug/Fix MRs:")
        for i, bug_title in enumerate(r['sample_bugs'][:5], 1):
            print(f"  {i}. {bug_title}")

    # Calculate team average
    if results:
        avg_bug_ratio = sum(r['bug_ratio'] for r in results) / len(results)
        print(f"\n{'='*80}")
        print(f"TEAM AVERAGE BUG RATIO: {avg_bug_ratio:.1f}%")
        print(f"{'='*80}\n")

if __name__ == '__main__':
    main()
