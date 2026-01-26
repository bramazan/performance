#!/usr/bin/env python3
"""Analyze Resul Bozdemir's GitLab Performance"""

import pandas as pd
import os
from datetime import datetime

print("="*100)
print("RESUL BOZDEMİR - GITLAB PERFORMANCE ANALYSIS 2025")
print("="*100)
print()

# Find the most recent file
resul_dir = 'user-metrics-resul'
files = os.listdir(resul_dir)
csv_file = [f for f in files if f.startswith('merge_requests_')]
xlsx_file = [f for f in files if f.startswith('metrics_')]

if not csv_file:
    print("❌ No data files found")
    exit(1)

# Read the merge requests CSV
mr_file = os.path.join(resul_dir, csv_file[0])
df = pd.read_csv(mr_file)

# Read the Excel summary
summary_file = os.path.join(resul_dir, xlsx_file[0])
summary_df = pd.read_excel(summary_file)

print(f"📊 Data loaded from: {mr_file}")
print(f"   Total Merge Requests: {len(df)}")
print()

# Convert dates
df['created_at'] = pd.to_datetime(df['created_at'])
df['merged_at'] = pd.to_datetime(df['merged_at'])
df['month'] = df['created_at'].dt.to_period('M')

# Basic stats
total_mrs = len(df)
merged_mrs = df['state'].value_counts().get('merged', 0)
merge_rate = (merged_mrs / total_mrs * 100) if total_mrs > 0 else 0

print(f"📋 OVERALL GITLAB STATISTICS")
print(f"   Total MRs: {total_mrs}")
print(f"   Merged: {merged_mrs} ({merge_rate:.1f}%)")
print(f"   State breakdown:")
for state, count in df['state'].value_counts().items():
    print(f"      • {state:15s}: {count:>3} ({count/total_mrs*100:>5.1f}%)")
print()

# Project breakdown
print(f"📂 PROJECT BREAKDOWN")
project_stats = df.groupby('project_name').agg({
    'id': 'count',
    'lines_added': 'sum',
    'lines_removed': 'sum',
    'lead_time_hours': 'mean'
}).rename(columns={'id': 'mrs'})

for project, row in project_stats.sort_values('mrs', ascending=False).iterrows():
    print(f"   • {project:40s}: {row['mrs']:>3} MRs | +{row['lines_added']:>5.0f} -{row['lines_removed']:>5.0f} lines | Avg Lead Time: {row['lead_time_hours']:>5.1f}h")
print()

# Monthly trend
print(f"📅 MONTHLY DISTRIBUTION")
monthly = df.groupby('month').agg({
    'id': 'count',
    'lines_added': 'sum',
    'lines_removed': 'sum',
    'lead_time_hours': 'mean'
}).rename(columns={'id': 'mrs'})

for month, row in monthly.iterrows():
    bar = '█' * min(int(row['mrs'] / 3), 30)
    print(f"   {month}: {row['mrs']:>3} MRs | +{row['lines_added']:>5.0f} -{row['lines_removed']:>5.0f} | Lead Time: {row['lead_time_hours']:>5.1f}h {bar}")
print()

# Complexity analysis based on lines changed
df['total_lines'] = df['lines_added'] + df['lines_removed']
df['complexity'] = pd.cut(
    df['total_lines'],
    bins=[0, 50, 200, float('inf')],
    labels=['Low', 'Medium', 'High']
)

print(f"🔍 MR COMPLEXITY ANALYSIS (Based on Lines Changed)")
for complexity in ['High', 'Medium', 'Low']:
    comp_df = df[df['complexity'] == complexity]
    count = len(comp_df)
    pct = count / total_mrs * 100
    avg_lines = comp_df['total_lines'].mean()
    avg_lead_time = comp_df['lead_time_hours'].mean()
    bar = '█' * int(pct / 2)
    print(f"   • {complexity:8s}: {count:>3} ({pct:>5.1f}%) | Avg Lines: {avg_lines:>6.1f} | Avg Lead Time: {avg_lead_time:>5.1f}h {bar}")
print()

# Lead time analysis
print(f"⏱️  LEAD TIME ANALYSIS")
print(f"   Average Lead Time: {df['lead_time_hours'].mean():.1f} hours ({df['lead_time_hours'].mean()/24:.1f} days)")
print(f"   Median Lead Time: {df['lead_time_hours'].median():.1f} hours ({df['lead_time_hours'].median()/24:.1f} days)")
print(f"   Min Lead Time: {df['lead_time_hours'].min():.1f} hours")
print(f"   Max Lead Time: {df['lead_time_hours'].max():.1f} hours ({df['lead_time_hours'].max()/24:.1f} days)")
print()

# Lines changed statistics
print(f"📈 CODE CHANGE STATISTICS")
print(f"   Total Lines Added: {df['lines_added'].sum():,}")
print(f"   Total Lines Removed: {df['lines_removed'].sum():,}")
print(f"   Total Lines Changed: {df['total_lines'].sum():,}")
print(f"   Avg Lines per MR: {df['total_lines'].mean():.1f}")
print(f"   Median Lines per MR: {df['total_lines'].median():.1f}")
print()

# Top 10 largest MRs
print(f"🌟 TOP 10 LARGEST MRs")
top_mrs = df.nlargest(10, 'total_lines')[['title', 'project_name', 'total_lines', 'lines_added', 'lines_removed', 'state']]
for idx, row in top_mrs.iterrows():
    print(f"   {row['total_lines']:>5.0f} lines | {row['project_name']:30s} | {row['state']:10s}")
    print(f"              (+{row['lines_added']:.0f} -{row['lines_removed']:.0f}) └─ {row['title'][:60]}")
print()

# Contribution type analysis (add vs remove ratio)
df['add_ratio'] = df['lines_added'] / (df['lines_added'] + df['lines_removed'] + 1)

print(f"🔧 CONTRIBUTION TYPE ANALYSIS")
new_features = df[df['add_ratio'] > 0.7]
refactoring = df[(df['add_ratio'] >= 0.3) & (df['add_ratio'] <= 0.7)]
deletions = df[df['add_ratio'] < 0.3]

print(f"   • New Features (>70% additions): {len(new_features)} MRs ({len(new_features)/total_mrs*100:.1f}%)")
print(f"   • Refactoring/Mixed (30-70%): {len(refactoring)} MRs ({len(refactoring)/total_mrs*100:.1f}%)")
print(f"   • Deletions/Cleanup (<30% additions): {len(deletions)} MRs ({len(deletions)/total_mrs*100:.1f}%)")
print()

# Summary metrics from Excel
print(f"📊 DORA METRICS SUMMARY (from Excel report)")
if not summary_df.empty:
    for _, row in summary_df.iterrows():
        print(f"   Metric: {row['Metric']}")
        print(f"   Value: {row['Value']}")
        print(f"   Assessment: {row['Assessment']}")
        print()

print("="*100)
print("✅ Analysis complete")
print("="*100)
