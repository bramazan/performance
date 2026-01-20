#!/usr/bin/env python3
"""Simple Jira Team Analysis"""

import requests
import pandas as pd
import re
from datetime import datetime


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
print(f"🎯 JIRA: {project} - 2025 Analysis")
print("=" * 100)
print()

# Fetch issues
url = f"{server}/rest/api/3/search/jql"
jql = f'project = {project} AND created >= "2025-01-01" AND created <= "2025-12-31" ORDER BY created DESC'

all_issues = []
start = 0

while True:
    params = {'jql': jql, 'startAt': start, 'maxResults': 100}

    r = requests.get(url, auth=(email, token), params=params)

    if r.status_code != 200:
        print(f"Error: {r.status_code}")
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

print(f"\n✅ Total: {len(all_issues)} issues\n")

# Parse
rows = []
for issue in all_issues:
    f = issue['fields']
    rows.append({
        'key': issue['key'],
        'summary': f.get('summary', ''),
        'type': f['issuetype']['name'] if 'issuetype' in f else 'Unknown',
        'status': f['status']['name'] if 'status' in f else 'Unknown',
        'created': f.get('created'),
        'assignee': f['assignee']['displayName'] if f.get('assignee') else 'Unassigned',
        'resolution': f['resolution']['name'] if f.get('resolution') else 'Unresolved',
    })

df = pd.DataFrame(rows)
df['created'] = pd.to_datetime(df['created']).dt.tz_localize(None)
df['month'] = df['created'].dt.to_period('M')

# Analysis
print("📊 RESULTS:")
print(f"   Total Issues: {len(df)}")
print(f"   Completed: {(df['status'] == 'Done').sum()} ({(df['status'] == 'Done').sum()/len(df)*100:.1f}%)")
print()

print("Issue Types:")
for t, c in df['type'].value_counts().items():
    print(f"   • {t:20s}: {c:>3} ({c/len(df)*100:>5.1f}%)")
print()

print("Monthly:")
for m, c in df.groupby('month').size().items():
    print(f"   {m}: {c} issues")
print()

print("Team Members:")
for a, c in df[df['assignee'] != 'Unassigned'].groupby('assignee').size().sort_values(ascending=False).items():
    print(f"   • {a:25s}: {c:>3} issues")

# Save
df.to_excel('jira-analysis/simple_analysis.xlsx', index=False)
df.to_csv('jira-analysis/simple_analysis.csv', index=False)
print("\n💾 Saved: jira-analysis/simple_analysis.xlsx")
