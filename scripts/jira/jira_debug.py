#!/usr/bin/env python3
"""Debug Jira API response"""

import requests
import json
import re

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

print(f"Server: {server}")
print(f"Project: {project}")
print(f"Email: {email}")
print()

# Fetch one issue
url = f"{server}/rest/api/3/search/jql"
jql = f'project = {project} AND created >= "2025-01-01" ORDER BY created DESC'

params = {
    'jql': jql,
    'startAt': 0,
    'maxResults': 2,
    'fields': 'summary,issuetype,status,created,assignee,reporter,resolution,description,priority,comment,labels,attachment,subtasks'
}

r = requests.get(url, auth=(email, token), params=params)

print(f"Status: {r.status_code}")
print()

if r.status_code == 200:
    data = r.json()
    print("Response structure:")
    print(json.dumps(data, indent=2)[:2000])
else:
    print(f"Error: {r.text}")
