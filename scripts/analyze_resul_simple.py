#!/usr/bin/env python3
"""Simple analysis of Resul Bozdemir's GitLab performance"""

import pandas as pd

print("="*100)
print("RESUL BOZDEMİR - GITLAB PERFORMANCE ANALYSIS 2025")
print("="*100)
print()

# Read Excel file
df = pd.read_excel('user-metrics-resul/metrics_resul_2026012023:27:14.xlsx')

# Filter only merged (those with merged_at)
print(f"📊 Total MRs: {len(df)}")
merged = df[df['merged_at'].notna()]
unmerged = df[df['merged_at'].isna()]

print(f"   Merged: {len(merged)} ({len(merged)/len(df)*100:.1f}%)")
print(f"   Not Merged: {len(unmerged)} ({len(unmerged)/len(df)*100:.1f}%)")
print()

# Parse project names from URLs
df['project_name'] = df['web_url'].str.extract(r'/odeal/([^/]+/[^/]+)/')

# Month analysis
df['created_at'] = pd.to_datetime(df['created_at'])
df['month'] = df['created_at'].dt.to_period('M')

# Monthly stats
print(f"📅 MONTHLY DISTRIBUTION")
monthly = merged.groupby('month').agg({
    'mr_id': 'count',
    'lead_time_hours': ['mean', 'median']
})
monthly.columns = ['mrs', 'avg_lead_time', 'median_lead_time']

for month, row in monthly.iterrows():
    bar = '█' * min(int(row['mrs'] / 2), 30)
    print(f"   {month}: {row['mrs']:>2} MRs | Avg Lead: {row['avg_lead_time']:>6.1f}h | Median: {row['median_lead_time']:>5.1f}h {bar}")
print()

# Project breakdown
print(f"📂 PROJECT BREAKDOWN")
project_stats = merged.groupby('project_name').agg({
    'mr_id': 'count',
    'lead_time_hours': 'mean'
}).sort_values('mr_id', ascending=False)

for project, row in project_stats.iterrows():
    print(f"   • {project:50s}: {row['mr_id']:>2} MRs | Avg Lead Time: {row['lead_time_hours']:>6.1f}h")
print()

# Lead time categorization
def categorize_lead_time(hours):
    if pd.isna(hours):
        return 'Not Merged'
    elif hours < 1:
        return 'Very Fast (<1h)'
    elif hours < 24:
        return 'Fast (<1 day)'
    elif hours < 72:
        return 'Medium (1-3 days)'
    elif hours < 168:
        return 'Slow (3-7 days)'
    else:
        return 'Very Slow (>1 week)'

df['lead_time_category'] = df['lead_time_hours'].apply(categorize_lead_time)

print(f"⏱️  LEAD TIME DISTRIBUTION")
for category in ['Very Fast (<1h)', 'Fast (<1 day)', 'Medium (1-3 days)', 'Slow (3-7 days)', 'Very Slow (>1 week)', 'Not Merged']:
    count = (df['lead_time_category'] == category).sum()
    pct = count / len(df) * 100
    bar = '█' * int(pct / 2)
    print(f"   • {category:20s}: {count:>2} ({pct:>5.1f}%) {bar}")
print()

# Top 5 fastest MRs
print(f"⚡ TOP 5 FASTEST MRs (Merged)")
fastest = merged.nsmallest(5, 'lead_time_hours')[['title', 'project_name', 'lead_time_hours']]
for idx, row in fastest.iterrows():
    print(f"   {row['lead_time_hours']:>6.2f}h | {row['project_name']:30s}")
    print(f"              └─ {row['title'][:70]}")
print()

# Top 5 slowest MRs
print(f"🐌 TOP 5 SLOWEST MRs (Merged)")
slowest = merged.nlargest(5, 'lead_time_hours')[['title', 'project_name', 'lead_time_hours']]
for idx, row in slowest.iterrows():
    days = row['lead_time_hours'] / 24
    print(f"   {row['lead_time_hours']:>7.1f}h ({days:>5.1f} days) | {row['project_name']:30s}")
    print(f"              └─ {row['title'][:70]}")
print()

# Not merged MRs
if len(unmerged) > 0:
    print(f"⚠️  NOT MERGED MRs ({len(unmerged)} total)")
    for idx, row in unmerged.iterrows():
        print(f"   {row['project_name']:40s} | {row['created_at'].strftime('%Y-%m-%d')}")
        print(f"              └─ {row['title'][:70]}")
    print()

# Overall stats
print(f"📈 SUMMARY STATISTICS")
print(f"   Total MRs: {len(df)}")
print(f"   Merge Rate: {len(merged)/len(df)*100:.1f}%")
print(f"   Avg Lead Time: {merged['lead_time_hours'].mean():.1f}h ({merged['lead_time_hours'].mean()/24:.1f} days)")
print(f"   Median Lead Time: {merged['lead_time_hours'].median():.1f}h ({merged['lead_time_hours'].median()/24:.1f} days)")
print(f"   Fastest MR: {merged['lead_time_hours'].min():.2f}h")
print(f"   Slowest MR: {merged['lead_time_hours'].max():.1f}h ({merged['lead_time_hours'].max()/24:.1f} days)")
print()

print("="*100)
print("✅ Analysis complete")
print("="*100)
