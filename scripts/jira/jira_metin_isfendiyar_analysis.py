#!/usr/bin/env python3
"""Jira Analysis for Metin İsfendiyar - Business Analyst Focus"""

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
project = link.split('/projects/')[1].split('/')[0]

email = config['EMAIL']
token = config['API_TOKEN']

print("=" * 100)
print(f"🎯 JIRA Analysis: Metin İsfendiyar - Business Analyst Performance 2025")
print("=" * 100)
print()

# Fetch all issues for 2025
url = f"{server}/rest/api/3/search/jql"
jql = f'project = {project} AND created >= "2025-01-01" AND created <= "2025-12-31" AND reporter = "Metin İsfendiyar" ORDER BY created DESC'

all_issues = []
start = 0

print("🔍 Fetching issues created by Metin İsfendiyar...")
while True:
    params = {'jql': jql, 'startAt': start, 'maxResults': 100}

    r = requests.get(url, auth=(email, token), params=params)

    if r.status_code != 200:
        print(f"❌ Error: {r.status_code}")
        print(r.text[:500])
        break

    data = r.json()
    issues = data.get('issues', data.get('values', []))

    if not issues:
        break

    all_issues.extend(issues)
    print(f"Fetched {len(all_issues)} issues...", end='\r')

    if len(all_issues) >= data.get('total', 0):
        break

    start += 100

print(f"\n✅ Total Issues Created by Metin: {len(all_issues)}\n")

if len(all_issues) == 0:
    print("⚠️  No issues found for Metin İsfendiyar in 2025")
    print("Trying alternative search...")
    # Try searching with assignee instead
    jql = f'project = {project} AND created >= "2025-01-01" AND created <= "2025-12-31" AND assignee = "Metin İsfendiyar" ORDER BY created DESC'

    start = 0
    while True:
        params = {'jql': jql, 'startAt': start, 'maxResults': 100}

        r = requests.get(url, auth=(email, token), params=params)

        if r.status_code != 200:
            print(f"❌ Error: {r.status_code}")
            print(r.text[:500])
            break

        data = r.json()
        issues = data.get('issues', data.get('values', []))

        if not issues:
            break

        all_issues.extend(issues)
        print(f"Fetched {len(all_issues)} issues...", end='\r')

        if len(all_issues) >= data.get('total', 0):
            break

        start += 100

    print(f"\n✅ Total Issues Assigned to Metin: {len(all_issues)}\n")

# Parse issues with detailed information
rows = []
for issue in all_issues:
    f = issue['fields']

    # Get description length as proxy for detail
    description = f.get('description', {})
    desc_text = ''
    if description and isinstance(description, dict):
        # Parse ADF (Atlassian Document Format)
        desc_content = description.get('content', [])
        for content_block in desc_content:
            if content_block.get('type') == 'paragraph':
                for text_item in content_block.get('content', []):
                    if text_item.get('type') == 'text':
                        desc_text += text_item.get('text', '')
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

    rows.append({
        'key': issue['key'],
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

# Save detailed data
df.to_excel('jira-analysis/metin_isfendiyar_analysis.xlsx', index=False)
df.to_csv('jira-analysis/metin_isfendiyar_analysis.csv', index=False)

# Analysis and reporting
print("=" * 100)
print("📊 METIN İSFENDİYAR - BUSINESS ANALYST PERFORMANCE REPORT")
print("=" * 100)
print()

# Basic stats
total_issues = len(df)
completed = (df['status'] == 'Done').sum()
in_progress = (df['status'] == 'In Progress').sum()
backlog = total_issues - completed - in_progress
completion_rate = (completed / total_issues * 100) if total_issues > 0 else 0

print(f"📋 OVERALL STATISTICS")
print(f"   Total Issues Created: {total_issues}")
print(f"   Completed: {completed} ({completion_rate:.1f}%)")
print(f"   In Progress: {in_progress} ({in_progress/total_issues*100:.1f}%)")
print(f"   Backlog: {backlog} ({backlog/total_issues*100:.1f}%)")
print()

# Issue types
print(f"📝 ISSUE TYPE DISTRIBUTION")
for t, c in df['type'].value_counts().items():
    print(f"   • {t:20s}: {c:>3} ({c/total_issues*100:>5.1f}%)")
print()

# Detail analysis
print(f"🔍 TASK DETAIL QUALITY ANALYSIS")
print(f"   Average Description Length: {df['description_words'].mean():.0f} words")
print(f"   Average Comments per Issue: {df['comment_count'].mean():.1f}")
print(f"   Average Attachments: {df['attachments'].mean():.1f}")
print(f"   Average Subtasks: {df['subtasks'].mean():.1f}")
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
    print(f"   {month}: {row['issues']:>3} issues (Avg Detail: {row['avg_detail']:.1f}/100)")
print()

# Priority distribution
print(f"⚡ PRIORITY DISTRIBUTION")
for p, c in df['priority'].value_counts().items():
    print(f"   • {p:15s}: {c:>3} ({c/total_issues*100:>5.1f}%)")
print()

# Top most detailed issues
print(f"🌟 TOP 10 MOST DETAILED ISSUES")
top_detailed = df.nlargest(10, 'detail_score')[['key', 'summary', 'type', 'detail_score', 'description_words', 'comment_count']]
for idx, row in top_detailed.iterrows():
    print(f"   {row['key']:10s} | Score: {row['detail_score']:>5.1f} | {row['type']:12s} | {row['description_words']:>3} words | {row['comment_count']:>2} comments")
    print(f"              └─ {row['summary'][:70]}")
print()

# Least detailed issues
print(f"⚠️  ISSUES NEEDING MORE DETAIL (Bottom 10)")
bottom_detailed = df.nsmallest(10, 'detail_score')[['key', 'summary', 'type', 'detail_score', 'description_words', 'comment_count']]
for idx, row in bottom_detailed.iterrows():
    print(f"   {row['key']:10s} | Score: {row['detail_score']:>5.1f} | {row['type']:12s} | {row['description_words']:>3} words | {row['comment_count']:>2} comments")
    print(f"              └─ {row['summary'][:70]}")
print()

print("=" * 100)
print("💾 Data saved to:")
print("   • jira-analysis/metin_isfendiyar_analysis.xlsx")
print("   • jira-analysis/metin_isfendiyar_analysis.csv")
print("=" * 100)
