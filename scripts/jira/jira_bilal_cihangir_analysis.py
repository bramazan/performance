#!/usr/bin/env python3
"""Jira Analysis for Bilal Cihangir - Product Owner Focus"""

import requests
import pandas as pd
import re
from datetime import datetime
from collections import Counter

# Parse env
config = {}
with open('jira.env', 'r') as f:
    for line in f:
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1)
            config[k.strip()] = v.strip()

# Extract from link
link = config['Jira_Link']
server = re.match(r'(https://[^/]+)', link).group(1)

email = config['EMAIL']
token = config['API_TOKEN']

print("=" * 100)
print(f"🎯 JIRA Analysis: Bilal Cihangir - Product Owner Performance 2025")
print("=" * 100)
print()

# Fetch all issues from both BPAY and TPAY for 2025
all_issues = []

for project in ['BPAY', 'TPAY']:
    print(f"🔍 Fetching {project} issues created/assigned to Bilal Cihangir...")

    url = f"{server}/rest/api/3/search/jql"
    jql = f'project = {project} AND created >= "2025-01-01" AND created <= "2025-12-31" AND (reporter = "Bilal Cihangir" OR assignee = "Bilal Cihangir") ORDER BY created DESC'

    start = 0
    project_issues = []

    while True:
        params = {'jql': jql, 'startAt': start, 'maxResults': 100}

        r = requests.get(url, auth=(email, token), params=params)

        if r.status_code != 200:
            print(f"❌ Error for {project}: {r.status_code}")
            print(r.text[:500])
            break

        data = r.json()
        issues = data.get('issues', data.get('values', []))

        if not issues:
            break

        # Add project tag to each issue
        for issue in issues:
            issue['_project'] = project

        project_issues.extend(issues)
        print(f"   Fetched {len(project_issues)} {project} issues...", end='\r')

        if len(project_issues) >= data.get('total', 0):
            break

        start += 100

    if project_issues:
        print(f"\n   ✅ Total {project} Issues: {len(project_issues)}")
        all_issues.extend(project_issues)
    else:
        print(f"\n   ⚠️  No {project} issues found")

print(f"\n✅ Grand Total Issues (BPAY + TPAY): {len(all_issues)}\n")

if len(all_issues) == 0:
    print("❌ No data found. Exiting...")
    exit(1)

# Parse issues with detailed information
rows = []
for issue in all_issues:
    f = issue['fields']

    # Get description length
    description = f.get('description', {})
    desc_text = ''
    if description and isinstance(description, dict):
        # Parse ADF (Atlassian Document Format)
        desc_content = description.get('content', [])
        for content_block in desc_content:
            if content_block.get('type') == 'paragraph':
                for text_item in content_block.get('content', []):
                    if text_item.get('type') == 'text':
                        desc_text += text_item.get('text', '') + ' '
    elif isinstance(description, str):
        desc_text = description

    desc_length = len(desc_text)
    desc_word_count = len(desc_text.split()) if desc_text else 0

    # Count comments
    comment_count = f.get('comment', {}).get('total', 0)

    # Get labels
    labels = f.get('labels', [])

    # Get priority
    priority = f.get('priority', {}).get('name', 'None') if f.get('priority') else 'None'

    # Get attachments
    attachments = len(f.get('attachment', []))

    # Get subtasks
    subtasks = len(f.get('subtasks', []))

    # Get story points (customfield_10016 is standard)
    story_points = f.get('customfield_10016', 0)

    rows.append({
        'key': issue['key'],
        'project': issue['_project'],
        'summary': f.get('summary', ''),
        'type': f['issuetype']['name'] if 'issuetype' in f else 'Unknown',
        'status': f['status']['name'] if 'status' in f else 'Unknown',
        'created': f.get('created'),
        'reporter': f.get('reporter', {}).get('displayName', 'Unknown'),
        'assignee': f['assignee']['displayName'] if f.get('assignee') else 'Unassigned',
        'resolution': f['resolution']['name'] if f.get('resolution') else 'Unresolved',
        'priority': priority,
        'description_length': desc_length,
        'description_words': desc_word_count,
        'comment_count': comment_count,
        'labels': ', '.join(labels) if labels else '',
        'attachments': attachments,
        'subtasks': subtasks,
        'story_points': story_points if story_points else 0,
    })

df = pd.DataFrame(rows)

if len(df) == 0:
    print("❌ No data found. Exiting...")
    exit(1)

df['created'] = pd.to_datetime(df['created']).dt.tz_localize(None)
df['month'] = df['created'].dt.to_period('M')

# Calculate detail score (0-100)
# Scoring: description words (40%), comments (30%), attachments (15%), subtasks (15%)
max_words = df['description_words'].max() if df['description_words'].max() > 0 else 1
max_comments = df['comment_count'].max() if df['comment_count'].max() > 0 else 1
max_attachments = df['attachments'].max() if df['attachments'].max() > 0 else 1
max_subtasks = df['subtasks'].max() if df['subtasks'].max() > 0 else 1

df['detail_score'] = (
    (df['description_words'] / max_words * 40) +
    (df['comment_count'] / max_comments * 30) +
    (df['attachments'] / max_attachments * 15) +
    (df['subtasks'] / max_subtasks * 15)
).round(1)

# Categorize by detail level
def categorize_detail(score):
    if score >= 70:
        return 'Excellent'
    elif score >= 50:
        return 'Good'
    elif score >= 30:
        return 'Fair'
    else:
        return 'Poor'

df['detail_category'] = df['detail_score'].apply(categorize_detail)

# Create output directory
import os
os.makedirs('../../results/2025/payment/bilal-cihangir', exist_ok=True)

# Save detailed data
df.to_excel('../../results/2025/payment/bilal-cihangir/jira_analysis.xlsx', index=False)
df.to_csv('../../results/2025/payment/bilal-cihangir/jira_analysis.csv', index=False)

print("=" * 100)
print("📊 BILAL CİHANGİR - PRODUCT OWNER PERFORMANCE REPORT")
print("=" * 100)
print()

# Basic stats
total_issues = len(df)
completed = (df['status'] == 'Done').sum()
closed = (df['status'] == 'Closed').sum()
backlog = (df['status'] == 'Backlog').sum()
in_progress = (df['status'] == 'In Progress').sum()
resolved = completed + closed
completion_rate = (resolved / total_issues * 100) if total_issues > 0 else 0

print(f"📋 OVERALL STATISTICS")
print(f"   Total Issues: {total_issues}")
print(f"   Completed (Done): {completed} ({completed/total_issues*100:.1f}%)")
print(f"   Closed: {closed} ({closed/total_issues*100:.1f}%)")
print(f"   Backlog: {backlog} ({backlog/total_issues*100:.1f}%)")
print(f"   In Progress: {in_progress} ({in_progress/total_issues*100:.1f}%)")
print(f"   Overall Completion Rate: {completion_rate:.1f}%")
print()

# Board distribution
print(f"📊 BOARD DISTRIBUTION")
bpay_count = (df['project'] == 'BPAY').sum()
tpay_count = (df['project'] == 'TPAY').sum()
print(f"   BPAY (Business Board): {bpay_count} ({bpay_count/total_issues*100:.1f}%)")
print(f"   TPAY (Tech Board): {tpay_count} ({tpay_count/total_issues*100:.1f}%)")
print()

# Issue types
print(f"📝 ISSUE TYPE DISTRIBUTION")
for t, c in df['type'].value_counts().items():
    type_completion = (df[df['type'] == t]['status'].isin(['Done', 'Closed'])).sum()
    type_rate = (type_completion / c * 100) if c > 0 else 0
    print(f"   • {t:25s}: {c:>3} ({c/total_issues*100:>5.1f}%) | Completed: {type_rate:.0f}%")
print()

# Detail analysis
print(f"🔍 TASK DETAIL QUALITY ANALYSIS")
print(f"   Average Description Length: {df['description_words'].mean():.0f} words")
print(f"   Average Comments per Issue: {df['comment_count'].mean():.1f}")
print(f"   Average Attachments: {df['attachments'].mean():.1f}")
print(f"   Average Subtasks: {df['subtasks'].mean():.1f}")
print(f"   Average Story Points: {df['story_points'].mean():.1f}")
print(f"   Average Detail Score: {df['detail_score'].mean():.1f}/100")
print()

print(f"   Detail Category Distribution:")
for cat in ['Excellent', 'Good', 'Fair', 'Poor']:
    count = (df['detail_category'] == cat).sum()
    pct = count / total_issues * 100
    print(f"   • {cat:12s}: {count:>3} ({pct:>5.1f}%)")
print()

# Monthly distribution
print(f"📅 MONTHLY DISTRIBUTION")
monthly = df.groupby('month').agg({
    'key': 'count',
    'detail_score': 'mean'
}).rename(columns={'key': 'issues', 'detail_score': 'avg_detail'})

for month, row in monthly.iterrows():
    month_issues = df[df['month'] == month]
    month_resolved = (month_issues['status'].isin(['Done', 'Closed'])).sum()
    month_rate = (month_resolved / row['issues'] * 100) if row['issues'] > 0 else 0
    bpay_m = (month_issues['project'] == 'BPAY').sum()
    tpay_m = (month_issues['project'] == 'TPAY').sum()
    print(f"   {month}: {row['issues']:>3} issues (BPAY:{bpay_m}, TPAY:{tpay_m}) | Detail:{row['avg_detail']:.0f} | Done:{month_rate:.0f}%")
print()

# Priority distribution
print(f"⚡ PRIORITY DISTRIBUTION")
for p, c in df['priority'].value_counts().items():
    print(f"   • {p:15s}: {c:>3} ({c/total_issues*100:>5.1f}%)")
print()

# Reporter vs Assignee
reporter_count = (df['reporter'] == 'Bilal Cihangir').sum()
assignee_count = (df['assignee'] == 'Bilal Cihangir').sum()
both_count = ((df['reporter'] == 'Bilal Cihangir') & (df['assignee'] == 'Bilal Cihangir')).sum()

print(f"👤 ROLE ANALYSIS")
print(f"   As Reporter (Created): {reporter_count} ({reporter_count/total_issues*100:.1f}%)")
print(f"   As Assignee (Assigned): {assignee_count} ({assignee_count/total_issues*100:.1f}%)")
print(f"   Both (Created & Assigned): {both_count} ({both_count/total_issues*100:.1f}%)")
print()

# Top issues by detail score
print(f"⭐ TOP 5 HIGHEST QUALITY ISSUES (Detail Score)")
top_issues = df.nlargest(5, 'detail_score')[['key', 'project', 'type', 'summary', 'detail_score', 'description_words', 'comment_count']]
for idx, row in top_issues.iterrows():
    print(f"   {row['key']:12} ({row['project']}) [{row['type']:15s}] Score:{row['detail_score']:>5.1f} | Words:{row['description_words']:>4} | Comments:{row['comment_count']}")
    print(f"                → {row['summary'][:70]}")
print()

# Bottom issues
print(f"⚠️  BOTTOM 5 LOWEST QUALITY ISSUES (Detail Score)")
bottom_issues = df.nsmallest(5, 'detail_score')[['key', 'project', 'type', 'summary', 'detail_score', 'description_words', 'comment_count']]
for idx, row in bottom_issues.iterrows():
    print(f"   {row['key']:12} ({row['project']}) [{row['type']:15s}] Score:{row['detail_score']:>5.1f} | Words:{row['description_words']:>4} | Comments:{row['comment_count']}")
    print(f"                → {row['summary'][:70]}")
print()

print("=" * 100)
print("✅ Analysis complete!")
print(f"📁 Detailed data exported to:")
print(f"   - ../../results/2025/payment/bilal-cihangir/jira_analysis.xlsx")
print(f"   - ../../results/2025/payment/bilal-cihangir/jira_analysis.csv")
print("=" * 100)

# Generate insights
print("\n" + "=" * 100)
print("💡 KEY INSIGHTS")
print("=" * 100)
print()

# Compare BPAY vs TPAY
bpay_df = df[df['project'] == 'BPAY']
tpay_df = df[df['project'] == 'TPAY']

if len(bpay_df) > 0:
    print(f"📊 BPAY (Business Board) Analysis:")
    print(f"   Total: {len(bpay_df)} issues ({len(bpay_df)/total_issues*100:.1f}%)")
    print(f"   Avg Detail Score: {bpay_df['detail_score'].mean():.1f}/100")
    print(f"   Avg Description: {bpay_df['description_words'].mean():.0f} words")
    print(f"   Completion Rate: {(bpay_df['status'].isin(['Done','Closed']).sum()/len(bpay_df)*100):.1f}%")
    print(f"   Top 3 Types: {dict(bpay_df['type'].value_counts().head(3))}")
    print()

if len(tpay_df) > 0:
    print(f"📊 TPAY (Tech Board) Analysis:")
    print(f"   Total: {len(tpay_df)} issues ({len(tpay_df)/total_issues*100:.1f}%)")
    print(f"   Avg Detail Score: {tpay_df['detail_score'].mean():.1f}/100")
    print(f"   Avg Description: {tpay_df['description_words'].mean():.0f} words")
    print(f"   Completion Rate: {(tpay_df['status'].isin(['Done','Closed']).sum()/len(tpay_df)*100):.1f}%")
    print(f"   Top 3 Types: {dict(tpay_df['type'].value_counts().head(3))}")
    print()

# Quarterly breakdown
print(f"📅 QUARTERLY BREAKDOWN")
df['quarter'] = df['created'].dt.quarter
quarterly = df.groupby('quarter').agg({
    'key': 'count',
    'detail_score': 'mean'
}).rename(columns={'key': 'issues', 'detail_score': 'avg_detail'})

for quarter, row in quarterly.iterrows():
    q_issues = df[df['quarter'] == quarter]
    q_bpay = (q_issues['project'] == 'BPAY').sum()
    q_tpay = (q_issues['project'] == 'TPAY').sum()
    q_resolved = (q_issues['status'].isin(['Done', 'Closed'])).sum()
    q_rate = (q_resolved / row['issues'] * 100) if row['issues'] > 0 else 0
    print(f"   Q{int(quarter)} 2025: {row['issues']:>2} issues (BPAY:{q_bpay}, TPAY:{q_tpay}) | Detail:{row['avg_detail']:.0f} | Done:{q_rate:.0f}%")

print("\n" + "=" * 100)
print("✅ Bilal Cihangir - Product Owner Analysis Complete!")
print("=" * 100)
