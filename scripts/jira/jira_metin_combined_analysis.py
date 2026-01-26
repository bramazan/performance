#!/usr/bin/env python3
"""Combined Jira Analysis for Metin İsfendiyar - TPAY + MU Projects"""

import requests
import pandas as pd
import re
from datetime import datetime
from collections import Counter
import os

# Parse env
config = {}
with open('jira.env', 'r') as f:
    for line in f:
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1)
            config[k.strip()] = v.strip()

server = "https://ode-al.atlassian.net"
projects = ["TPAY", "MU"]

email = config['EMAIL']
token = config['API_TOKEN']

print("=" * 100)
print(f"🎯 JIRA Combined Analysis: Metin İsfendiyar - Business Analyst Performance 2025")
print(f"📋 Projects: {', '.join(projects)}")
print("=" * 100)
print()

all_issues_combined = []
metin_name = None

for project in projects:
    print(f"\n{'='*100}")
    print(f"📂 Analyzing Project: {project}")
    print(f"{'='*100}\n")

    url = f"{server}/rest/api/3/search/jql"
    jql = f'project = {project} AND created >= "2025-01-01" AND created <= "2025-12-31" ORDER BY created DESC'

    # Sample to find Metin
    print(f"🔍 Finding users in {project}...")
    sample_issues = []
    start = 0

    while start < 200:
        params = {
            'jql': jql,
            'startAt': start,
            'maxResults': 100,
            'fields': 'reporter,assignee'
        }

        r = requests.get(url, auth=(email, token), params=params)

        if r.status_code != 200:
            print(f"❌ Error: {r.status_code}")
            break

        data = r.json()
        issues = data.get('issues', [])

        if not issues:
            break

        sample_issues.extend(issues)
        start += 100

    # Find Metin
    reporters = set()
    for issue in sample_issues:
        if 'fields' in issue:
            reporter = issue['fields'].get('reporter', {})
            if reporter:
                reporters.add(reporter.get('displayName', 'Unknown'))

    metin_variations = [name for name in reporters if 'metin' in name.lower() or 'isfendiyar' in name.lower()]

    if not metin_variations:
        print(f"⚠️  No user found with 'Metin' in {project}")
        continue

    if metin_name is None:
        metin_name = metin_variations[0]

    print(f"✅ Found: {metin_name}")

    # Fetch all issues created by Metin
    print(f"🔍 Fetching all issues created by {metin_name} in {project}...")
    jql_metin = f'project = {project} AND created >= "2025-01-01" AND created <= "2025-12-31" AND reporter = "{metin_name}" ORDER BY created DESC'

    project_issues = []
    start = 0

    while True:
        params = {
            'jql': jql_metin,
            'startAt': start,
            'maxResults': 100,
            'fields': 'summary,issuetype,status,created,assignee,reporter,resolution,description,priority,comment,labels,attachment,subtasks,project'
        }

        r = requests.get(url, auth=(email, token), params=params)

        if r.status_code != 200:
            print(f"❌ Error: {r.status_code}")
            break

        data = r.json()
        issues = data.get('issues', [])

        if not issues:
            break

        project_issues.extend(issues)
        print(f"Fetched {len(project_issues)} issues from {project}...", end='\r')

        start += 100

    print(f"\n✅ {project}: {len(project_issues)} issues")
    all_issues_combined.extend(project_issues)

print(f"\n{'='*100}")
print(f"✅ TOTAL Issues Created by {metin_name}: {len(all_issues_combined)}")
print(f"{'='*100}\n")

if len(all_issues_combined) == 0:
    print("❌ No issues found. Exiting...")
    exit(1)

# Parse all issues
rows = []
for issue in all_issues_combined:
    f = issue['fields']

    # Get description
    description = f.get('description', {})
    desc_text = ''
    if description and isinstance(description, dict):
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

    comment_count = f.get('comment', {}).get('total', 0)
    labels = f.get('labels', [])
    priority = f.get('priority', {}).get('name', 'None') if f.get('priority') else 'None'
    attachments = len(f.get('attachment', []))
    subtasks = len(f.get('subtasks', []))
    project_key = f.get('project', {}).get('key', 'Unknown')

    rows.append({
        'project': project_key,
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
df['created'] = pd.to_datetime(df['created']).dt.tz_localize(None)
df['month'] = df['created'].dt.to_period('M')

# Calculate detail score
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

# Save
os.makedirs('jira-analysis', exist_ok=True)
df.to_excel('jira-analysis/metin_isfendiyar_combined_analysis.xlsx', index=False)
df.to_csv('jira-analysis/metin_isfendiyar_combined_analysis.csv', index=False)

# Generate report
print("=" * 100)
print(f"📊 {metin_name.upper()} - BUSINESS ANALYST PERFORMANCE REPORT (COMBINED)")
print("=" * 100)
print()

total_issues = len(df)
completed = (df['status'] == 'Done').sum()
in_progress = (df['status'].isin(['In Progress', 'In Review', 'Testing', 'To Do'])).sum()
backlog = total_issues - completed - in_progress
completion_rate = (completed / total_issues * 100) if total_issues > 0 else 0

print(f"📋 OVERALL STATISTICS")
print(f"   Total Issues Created: {total_issues}")
print(f"   Completed: {completed} ({completion_rate:.1f}%)")
print(f"   In Progress/To Do: {in_progress} ({in_progress/total_issues*100:.1f}%)")
print(f"   Other: {backlog} ({backlog/total_issues*100:.1f}%)")
print()

# Project breakdown
print(f"📂 PROJECT BREAKDOWN")
for proj, count in df['project'].value_counts().items():
    print(f"   • {proj:10s}: {count:>3} issues ({count/total_issues*100:>5.1f}%)")
print()

# Issue types
print(f"📝 ISSUE TYPE DISTRIBUTION")
for t, c in df['type'].value_counts().items():
    print(f"   • {t:20s}: {c:>3} ({c/total_issues*100:>5.1f}%)")
print()

# Detail analysis
print(f"🔍 TASK DETAIL QUALITY ANALYSIS (IŞ ANALİSTİ → PRODUCT OWNER GEÇİŞ)")
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
    bar = '█' * int(pct / 2)
    print(f"   • {cat:12s}: {count:>3} ({pct:>5.1f}%) {bar}")
print()

# Assessment
avg_score = df['detail_score'].mean()
excellent_pct = (df['detail_category'] == 'Excellent').sum() / total_issues * 100
poor_pct = (df['detail_category'] == 'Poor').sum() / total_issues * 100

print(f"📈 OVERALL ASSESSMENT:")
if avg_score >= 60:
    print(f"   ⭐⭐⭐ EXCELLENT - Tasks are well-detailed and ready for handoff")
elif avg_score >= 45:
    print(f"   ⭐⭐ GOOD - Most tasks have sufficient detail")
elif avg_score >= 30:
    print(f"   ⭐ FAIR - Tasks need more detail for product ownership")
else:
    print(f"   ⚠️  NEEDS IMPROVEMENT - Significant detail gaps")

print()

# Monthly distribution
print(f"📅 MONTHLY DISTRIBUTION & TREND")
monthly = df.groupby('month').agg({
    'key': 'count',
    'detail_score': 'mean'
}).rename(columns={'key': 'issues', 'detail_score': 'avg_detail'})

for month, row in monthly.iterrows():
    bar = '█' * min(int(row['issues'] / 3), 30)
    detail_indicator = '⭐' if row['avg_detail'] >= 60 else '✓' if row['avg_detail'] >= 45 else '○'
    print(f"   {month}: {row['issues']:>3} issues (Detail: {row['avg_detail']:.1f}/100 {detail_indicator}) {bar}")
print()

# Priority distribution
print(f"⚡ PRIORITY DISTRIBUTION")
for p, c in df['priority'].value_counts().items():
    print(f"   • {p:15s}: {c:>3} ({c/total_issues*100:>5.1f}%)")
print()

# Status distribution
print(f"📊 STATUS DISTRIBUTION")
for s, c in df['status'].value_counts().items():
    print(f"   • {s:20s}: {c:>3} ({c/total_issues*100:>5.1f}%)")
print()

# Top most detailed
print(f"🌟 TOP 10 MOST DETAILED ISSUES (ÖRNEK BAŞARILI TASKLAR)")
top_detailed = df.nlargest(min(10, len(df)), 'detail_score')[['project', 'key', 'summary', 'type', 'detail_score', 'description_words', 'comment_count']]
for idx, row in top_detailed.iterrows():
    print(f"   [{row['project']}] {row['key']:10s} | Score: {row['detail_score']:>5.1f} | {row['type']:12s}")
    print(f"              Words: {row['description_words']:>3} | Comments: {row['comment_count']:>2} | {row['summary'][:60]}")
print()

# Least detailed
print(f"⚠️  ISSUES NEEDING MORE DETAIL (GELİŞTİRME ALANLARI)")
bottom_detailed = df.nsmallest(min(10, len(df)), 'detail_score')[['project', 'key', 'summary', 'type', 'detail_score', 'description_words', 'comment_count']]
for idx, row in bottom_detailed.iterrows():
    print(f"   [{row['project']}] {row['key']:10s} | Score: {row['detail_score']:>5.1f} | {row['type']:12s}")
    print(f"              Words: {row['description_words']:>3} | Comments: {row['comment_count']:>2} | {row['summary'][:60]}")
print()

print("=" * 100)
print("💡 KEY INSIGHTS FOR PRODUCT OWNER TRANSITION:")
print("=" * 100)

# Insights
insights = []

if completion_rate >= 70:
    insights.append(f"✅ Strong delivery rate ({completion_rate:.0f}%) - good task closure discipline")
else:
    insights.append(f"⚠️  Completion rate ({completion_rate:.0f}%) could be improved")

if avg_score >= 60:
    insights.append(f"✅ Excellent task detail quality (avg: {avg_score:.0f}/100)")
elif avg_score >= 45:
    insights.append(f"⭐ Good task detail quality (avg: {avg_score:.0f}/100) - minor improvements possible")
else:
    insights.append(f"⚠️  Task detail needs improvement (avg: {avg_score:.0f}/100)")

if excellent_pct >= 40:
    insights.append(f"✅ {excellent_pct:.0f}% of tasks are excellently detailed")
elif poor_pct >= 40:
    insights.append(f"⚠️  {poor_pct:.0f}% of tasks lack sufficient detail")

if df['comment_count'].mean() >= 3:
    insights.append(f"✅ Good collaboration (avg {df['comment_count'].mean():.1f} comments per task)")
else:
    insights.append(f"💡 More discussion/clarification could improve task quality")

if df['attachments'].mean() >= 0.5:
    insights.append(f"✅ Good use of attachments for documentation")

for insight in insights:
    print(f"   {insight}")

print()
print("=" * 100)
print("💾 Data saved to:")
print("   • jira-analysis/metin_isfendiyar_combined_analysis.xlsx")
print("   • jira-analysis/metin_isfendiyar_combined_analysis.csv")
print("=" * 100)
