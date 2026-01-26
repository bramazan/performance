#!/usr/bin/env python3
"""List all Jira users in the project"""

import requests
import pandas as pd
import re
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
print(f"🎯 JIRA Users in Project: {project}")
print("=" * 100)
print()

# Fetch all issues for 2025
url = f"{server}/rest/api/3/search/jql"
jql = f'project = {project} AND created >= "2025-01-01" AND created <= "2025-12-31" ORDER BY created DESC'

all_issues = []
start = 0

print("🔍 Fetching all issues to extract user list...")
while True:
    params = {
        'jql': jql,
        'startAt': start,
        'maxResults': 100,
        'fields': 'reporter,assignee'
    }

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

print(f"\n✅ Total Issues: {len(all_issues)}\n")

# Extract all reporters and assignees
reporters = []
assignees = []

for issue in all_issues:
    if 'fields' not in issue:
        continue

    f = issue['fields']

    reporter = f.get('reporter', {})
    if reporter:
        reporters.append(reporter.get('displayName', 'Unknown'))

    assignee = f.get('assignee', {})
    if assignee:
        assignees.append(assignee.get('displayName', 'Unknown'))

# Count and display
print("📊 REPORTERS (Issue Creators):")
reporter_counts = Counter(reporters)
for name, count in reporter_counts.most_common(50):
    print(f"   • {name:40s}: {count:>4} issues")

print("\n" + "=" * 100)
print("\n📊 ASSIGNEES (Issue Owners):")
assignee_counts = Counter(assignees)
for name, count in assignee_counts.most_common(50):
    print(f"   • {name:40s}: {count:>4} issues")

print("\n" + "=" * 100)

# Search for Metin
print("\n🔍 Searching for 'Metin' or 'İsfendiyar'...")
all_names = set(reporters + assignees)
matching = [name for name in all_names if 'metin' in name.lower() or 'isfendiyar' in name.lower()]

if matching:
    print("✅ Found matches:")
    for name in matching:
        print(f"   • {name}")
else:
    print("❌ No matches found for 'Metin' or 'İsfendiyar'")

print("\n" + "=" * 100)
