#!/usr/bin/env python3
"""Jira Analysis for Resul Bozdemir - TSB + TPAY Projects"""

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
projects = ["TSB", "TPAY"]  # Service Banking & Payment

email = config['EMAIL']
token = config['API_TOKEN']

print("=" * 100)
print(f"🎯 JIRA Analysis: Resul Bozdemir - Developer Performance 2025")
print(f"📋 Projects: {', '.join(projects)}")
print("=" * 100)
print()

all_issues_combined = []
resul_name = None

for project in projects:
    print(f"\n{'='*100}")
    print(f"📂 Analyzing Project: {project}")
    print(f"{'='*100}\n")

    url = f"{server}/rest/api/3/search/jql"
    jql = f'project = {project} AND created >= "2025-01-01" AND created <= "2025-12-31" ORDER BY created DESC'

    # Sample to find Resul
    print(f"🔍 Finding users in {project}...")
    sample_issues = []
    start = 0

    while start < 200:
        params = {
            'jql': jql,
            'startAt': start,
            'maxResults': 100,
            'fields': 'assignee,reporter'
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

    # Find Resul (check both assignee and reporter)
    assignees = set()
    reporters = set()
    for issue in sample_issues:
        if 'fields' in issue:
            assignee = issue['fields'].get('assignee', {})
            if assignee:
                assignees.add(assignee.get('displayName', 'Unknown'))
            reporter = issue['fields'].get('reporter', {})
            if reporter:
                reporters.add(reporter.get('displayName', 'Unknown'))

    all_users = assignees.union(reporters)
    resul_variations = [name for name in all_users if 'resul' in name.lower() or 'bozdemir' in name.lower()]

    if not resul_variations:
        print(f"⚠️  No user found with 'Resul' in {project}")
        continue

    if resul_name is None:
        resul_name = resul_variations[0]

    print(f"✅ Found: {resul_name}")

    # Fetch all issues assigned to Resul
    print(f"🔍 Fetching all issues assigned to {resul_name} in {project}...")
    jql_resul = f'project = {project} AND created >= "2025-01-01" AND created <= "2025-12-31" AND assignee = "{resul_name}" ORDER BY created DESC'

    project_issues = []
    start = 0

    while True:
        params = {
            'jql': jql_resul,
            'startAt': start,
            'maxResults': 100,
            'fields': 'summary,issuetype,status,created,assignee,reporter,resolution,description,priority,comment,labels,attachment,subtasks,project,timetracking,timespent,timeestimate'
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
print(f"✅ TOTAL Issues Assigned to {resul_name}: {len(all_issues_combined)}")
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

    # Time tracking
    time_spent = f.get('timespent', 0) or 0  # In seconds
    time_estimate = f.get('timeestimate', 0) or 0  # In seconds

    # Calculate complexity score based on:
    # - Description length
    # - Subtasks
    # - Comments
    # - Attachments
    complexity_score = 0
    if desc_word_count > 200:
        complexity_score += 3
    elif desc_word_count > 100:
        complexity_score += 2
    elif desc_word_count > 50:
        complexity_score += 1

    complexity_score += min(subtasks, 3)  # Max 3 points for subtasks
    complexity_score += min(comment_count // 3, 2)  # Max 2 points for comments
    complexity_score += min(attachments, 2)  # Max 2 points for attachments

    # Categorize complexity
    if complexity_score >= 7:
        complexity = 'High'
    elif complexity_score >= 4:
        complexity = 'Medium'
    else:
        complexity = 'Low'

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
        'time_spent_hours': time_spent / 3600 if time_spent else 0,
        'time_estimate_hours': time_estimate / 3600 if time_estimate else 0,
        'complexity_score': complexity_score,
        'complexity': complexity,
    })

df = pd.DataFrame(rows)
df['created'] = pd.to_datetime(df['created']).dt.tz_localize(None)
df['month'] = df['created'].dt.to_period('M')

# Save
os.makedirs('jira-analysis', exist_ok=True)
df.to_excel('jira-analysis/resul_bozdemir_analysis.xlsx', index=False)
df.to_csv('jira-analysis/resul_bozdemir_analysis.csv', index=False)

# Generate report
print("=" * 100)
print(f"📊 {resul_name.upper()} - DEVELOPER PERFORMANCE REPORT")
print("=" * 100)
print()

total_issues = len(df)
completed = (df['status'] == 'Done').sum()
in_progress = (df['status'].isin(['In Progress', 'In Review', 'Testing', 'To Do'])).sum()
backlog = total_issues - completed - in_progress
completion_rate = (completed / total_issues * 100) if total_issues > 0 else 0

print(f"📋 OVERALL STATISTICS")
print(f"   Total Issues Assigned: {total_issues}")
print(f"   Completed: {completed} ({completion_rate:.1f}%)")
print(f"   In Progress/To Do: {in_progress} ({in_progress/total_issues*100:.1f}%)")
print(f"   Other: {backlog} ({backlog/total_issues*100:.1f}%)")
print()

# Project breakdown
print(f"📂 PROJECT BREAKDOWN")
for proj, count in df['project'].value_counts().items():
    proj_completed = (df[df['project'] == proj]['status'] == 'Done').sum()
    proj_completion = (proj_completed / count * 100) if count > 0 else 0
    print(f"   • {proj:10s}: {count:>3} issues | Completion: {proj_completion:.1f}% ({proj_completed}/{count})")
print()

# Issue types
print(f"📝 ISSUE TYPE DISTRIBUTION")
for itype, c in df['type'].value_counts().items():
    type_completed = (df[df['type'] == itype]['status'] == 'Done').sum()
    type_completion = (type_completed / c * 100) if c > 0 else 0
    print(f"   • {itype:20s}: {c:>3} ({c/total_issues*100:>5.1f}%) | Completion: {type_completion:.1f}%")
print()

# Complexity analysis
print(f"🔍 TASK COMPLEXITY ANALYSIS")
for complexity in ['High', 'Medium', 'Low']:
    count = (df['complexity'] == complexity).sum()
    pct = count / total_issues * 100
    comp_completed = (df[df['complexity'] == complexity]['status'] == 'Done').sum()
    comp_completion = (comp_completed / count * 100) if count > 0 else 0
    bar = '█' * int(pct / 2)
    print(f"   • {complexity:8s}: {count:>3} ({pct:>5.1f}%) | Completion: {comp_completion:>5.1f}% {bar}")
print()

# Monthly distribution
print(f"📅 MONTHLY DISTRIBUTION")
monthly = df.groupby('month').agg({
    'key': 'count',
    'complexity_score': 'mean'
}).rename(columns={'key': 'issues', 'complexity_score': 'avg_complexity'})

for month, row in monthly.iterrows():
    bar = '█' * min(int(row['issues'] / 3), 30)
    print(f"   {month}: {row['issues']:>3} issues (Avg Complexity: {row['avg_complexity']:.1f}/10) {bar}")
print()

# Priority distribution
print(f"⚡ PRIORITY DISTRIBUTION")
for p, c in df['priority'].value_counts().items():
    priority_completed = (df[df['priority'] == p]['status'] == 'Done').sum()
    priority_completion = (priority_completed / c * 100) if c > 0 else 0
    print(f"   • {p:15s}: {c:>3} ({c/total_issues*100:>5.1f}%) | Completion: {priority_completion:.1f}%")
print()

# Status distribution
print(f"📊 STATUS DISTRIBUTION")
for s, c in df['status'].value_counts().items():
    print(f"   • {s:20s}: {c:>3} ({c/total_issues*100:>5.1f}%)")
print()

# Completion by complexity
print(f"✅ COMPLETION RATE BY COMPLEXITY")
for complexity in ['High', 'Medium', 'Low']:
    comp_df = df[df['complexity'] == complexity]
    done_count = (comp_df['status'] == 'Done').sum()
    completion = done_count / len(comp_df) * 100 if len(comp_df) > 0 else 0
    avg_comments = comp_df['comment_count'].mean()
    avg_subtasks = comp_df['subtasks'].mean()
    print(f"   • {complexity:8s}: {done_count:>3}/{len(comp_df):<3} ({completion:>5.1f}%) | Avg Comments: {avg_comments:.1f} | Avg Subtasks: {avg_subtasks:.1f}")
print()

# Top complex tasks
print(f"🌟 TOP 10 MOST COMPLEX TASKS")
top_complex = df.nlargest(10, 'complexity_score')[['project', 'key', 'summary', 'type', 'complexity', 'complexity_score', 'status']]
for idx, row in top_complex.iterrows():
    print(f"   [{row['project']}] {row['key']:10s} | {row['complexity']:8s} ({row['complexity_score']:>2}/10) | {row['type']:12s} | {row['status']:15s}")
    print(f"              └─ {row['summary'][:70]}")
print()

# Simplest completed tasks
print(f"⚡ TOP 10 SIMPLEST TASKS (Low Complexity)")
simple_tasks = df[df['complexity'] == 'Low'].nsmallest(10, 'complexity_score')[['project', 'key', 'summary', 'type', 'complexity_score', 'status']]
for idx, row in simple_tasks.iterrows():
    print(f"   [{row['project']}] {row['key']:10s} | Score: {row['complexity_score']:>2}/10 | {row['type']:12s} | {row['status']:15s}")
    print(f"              └─ {row['summary'][:70]}")
print()

print("=" * 100)
print("💾 Data saved to:")
print("   • jira-analysis/resul_bozdemir_analysis.xlsx")
print("   • jira-analysis/resul_bozdemir_analysis.csv")
print("=" * 100)
