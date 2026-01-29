#!/usr/bin/env python3
"""
Jira Payment Team - Product Owner & Business Analyst Analysis
Analyzes both BPAY (Business Board) and TPAY (Tech Board)
For: Tahsin Civelek, Bilal Cihangir, Metin İsfendiyar
"""

import requests
import pandas as pd
import re
from datetime import datetime
from collections import Counter

# Parse config
config = {}
with open('jira.env', 'r') as f:
    for line in f:
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1)
            config[k.strip()] = v.strip()

server_match = re.match(r'(https://[^/]+)', config.get('Jira_Link', ''))
server = server_match.group(1) if server_match else "https://odeal.atlassian.net"

email = config['EMAIL']
token = config['API_TOKEN']

# Team members to analyze
TEAM = {
    "Metin İsfendiyar": {"role": "Business Analyst", "primary_board": "TPAY"},
    "Tahsin Civelek": {"role": "Product Owner", "primary_board": "BPAY"},
    "Bilal Cihangir": {"role": "Product Owner", "primary_board": "BPAY"}
}

print("=" * 100)
print("🎯 PAYMENT TEAM - PRODUCT OWNER & BUSINESS ANALYST ANALYSIS")
print("📅 Period: 2025-01-01 to 2025-12-31")
print("🔗 Boards: BPAY (Business) + TPAY (Tech)")
print("=" * 100)

url = f"{server}/rest/api/3/search/jql"

def fetch_jira_issues(person_name, project, role_type="reporter"):
    """Fetch all issues for a person in a project"""
    all_issues = []
    start = 0

    jql = f'project = {project} AND created >= "2025-01-01" AND created <= "2025-12-31" AND {role_type} = "{person_name}" ORDER BY created DESC'

    while start < 2000:  # Safety limit
        params = {
            'jql': jql,
            'startAt': start,
            'maxResults': 100,
            'fields': 'summary,description,issuetype,status,priority,reporter,assignee,created,updated,resolutiondate,comment,labels,customfield_10016'  # customfield_10016 is usually story points
        }

        try:
            r = requests.get(url, auth=(email, token), params=params, timeout=30)

            if r.status_code != 200:
                print(f"       Error {r.status_code}")
                break

            data = r.json()
            issues = data.get('issues', [])

            if not issues:
                break

            all_issues.extend(issues)
            print(f"       Fetched {len(all_issues)} issues...", end='\r')

            if len(all_issues) >= data.get('total', 0):
                break

            start += 100

        except Exception as e:
            print(f"       Exception: {str(e)[:60]}")
            break

    return all_issues


def analyze_issues(issues, person_name):
    """Analyze issues for quality metrics"""

    if not issues:
        return None

    metrics = {
        'total_issues': len(issues),
        'issue_types': Counter(),
        'statuses': Counter(),
        'priorities': Counter(),
        'resolved_count': 0,
        'as_reporter': 0,
        'as_assignee': 0,
        'total_comments': 0,
        'with_description': 0,
        'total_description_length': 0,
        'with_labels': 0,
        'story_points_total': 0,
        'story_points_count': 0,
        'issue_details': []
    }

    for issue in issues:
        fields = issue.get('fields', {})
        key = issue.get('key', 'Unknown')

        # Issue type
        issue_type = fields.get('issuetype', {}).get('name', 'Unknown')
        metrics['issue_types'][issue_type] += 1

        # Status
        status = fields.get('status', {}).get('name', 'Unknown')
        metrics['statuses'][status] += 1

        # Priority
        priority = fields.get('priority', {}).get('name', 'None')
        metrics['priorities'][priority] += 1

        # Reporter vs Assignee
        reporter = fields.get('reporter', {})
        if reporter and person_name.lower() in reporter.get('displayName', '').lower():
            metrics['as_reporter'] += 1

        assignee = fields.get('assignee', {})
        if assignee and person_name.lower() in assignee.get('displayName', '').lower():
            metrics['as_assignee'] += 1

        # Resolution
        if fields.get('resolutiondate'):
            metrics['resolved_count'] += 1

        # Description quality
        desc = fields.get('description')
        desc_length = 0
        if desc:
            metrics['with_description'] += 1
            # Extract text from ADF format
            if isinstance(desc, dict):
                desc_text = extract_text_from_adf(desc)
                desc_length = len(desc_text)
                metrics['total_description_length'] += desc_length

        # Comments
        comments = fields.get('comment', {}).get('comments', [])
        metrics['total_comments'] += len(comments)

        # Labels
        labels = fields.get('labels', [])
        if labels:
            metrics['with_labels'] += 1

        # Story points
        story_points = fields.get('customfield_10016')  # Standard story points field
        if story_points:
            metrics['story_points_total'] += float(story_points)
            metrics['story_points_count'] += 1

        # Store issue details
        metrics['issue_details'].append({
            'key': key,
            'type': issue_type,
            'status': status,
            'summary': fields.get('summary', 'No summary')[:100],
            'created': fields.get('created', ''),
            'resolved': fields.get('resolutiondate', ''),
            'desc_length': desc_length,
            'comments': len(comments)
        })

    # Calculate aggregate metrics
    metrics['completion_rate'] = (metrics['resolved_count'] / metrics['total_issues'] * 100) if metrics['total_issues'] > 0 else 0
    metrics['avg_description_length'] = metrics['total_description_length'] / metrics['with_description'] if metrics['with_description'] > 0 else 0
    metrics['avg_comments_per_issue'] = metrics['total_comments'] / metrics['total_issues'] if metrics['total_issues'] > 0 else 0
    metrics['description_coverage'] = (metrics['with_description'] / metrics['total_issues'] * 100) if metrics['total_issues'] > 0 else 0
    metrics['label_usage'] = (metrics['with_labels'] / metrics['total_issues'] * 100) if metrics['total_issues'] > 0 else 0
    metrics['avg_story_points'] = metrics['story_points_total'] / metrics['story_points_count'] if metrics['story_points_count'] > 0 else 0

    return metrics


def extract_text_from_adf(adf_content):
    """Extract plain text from Atlassian Document Format"""
    text = ""

    if isinstance(adf_content, dict):
        content_blocks = adf_content.get('content', [])
        for block in content_blocks:
            if isinstance(block, dict):
                block_type = block.get('type', '')
                if block_type == 'paragraph':
                    paragraph_content = block.get('content', [])
                    for text_block in paragraph_content:
                        if isinstance(text_block, dict) and text_block.get('type') == 'text':
                            text += text_block.get('text', '') + " "
                elif 'content' in block:
                    text += extract_text_from_adf(block) + " "

    return text.strip()


# Main analysis
all_results = {}

for person_name, person_info in TEAM.items():
    print(f"\n{'='*100}")
    print(f"👤 {person_name} ({person_info['role']})")
    print(f"{'='*100}")

    person_results = {}

    # Analyze both boards
    for project in ['BPAY', 'TPAY']:
        print(f"\n  📊 {project} Board:")

        # Try as reporter first
        print(f"     Checking as reporter...")
        issues = fetch_jira_issues(person_name, project, "reporter")

        # If no issues as reporter, try assignee
        if not issues:
            print(f"\n     Checking as assignee...")
            issues = fetch_jira_issues(person_name, project, "assignee")

        if issues:
            print(f"\n     ✅ Found {len(issues)} issues")
            metrics = analyze_issues(issues, person_name)

            if metrics:
                person_results[project] = metrics

                print(f"\n     📈 Quick Stats:")
                print(f"        Total Issues: {metrics['total_issues']}")
                print(f"        As Reporter: {metrics['as_reporter']}")
                print(f"        As Assignee: {metrics['as_assignee']}")
                print(f"        Completion Rate: {metrics['completion_rate']:.1f}%")
                print(f"        Avg Description Length: {metrics['avg_description_length']:.0f} chars")
                print(f"        Avg Comments/Issue: {metrics['avg_comments_per_issue']:.1f}")
                print(f"\n        Issue Types: {dict(metrics['issue_types'])}")
        else:
            print(f"\n     ⚠️  No issues found")

    all_results[person_name] = person_results

# Generate summary report
print(f"\n{'='*100}")
print("📊 COMPREHENSIVE SUMMARY")
print(f"{'='*100}\n")

for person, data in all_results.items():
    total_issues = sum(board_data.get('total_issues', 0) for board_data in data.values())

    if total_issues > 0:
        print(f"\n{person}:")
        print(f"  Total Issues: {total_issues}")

        for board, metrics in data.items():
            print(f"\n  {board} Board ({metrics['total_issues']} issues):")
            print(f"    Created (Reporter): {metrics['as_reporter']}")
            print(f"    Assigned: {metrics['as_assignee']}")
            print(f"    Completion Rate: {metrics['completion_rate']:.1f}%")
            print(f"    Issue Types: {dict(metrics['issue_types'])}")
            print(f"    Top 3 Statuses: {dict(metrics['statuses'].most_common(3))}")
            print(f"    Description Coverage: {metrics['description_coverage']:.1f}%")
            print(f"    Avg Comments/Issue: {metrics['avg_comments_per_issue']:.1f}")

            if metrics['story_points_count'] > 0:
                print(f"    Story Points (avg): {metrics['avg_story_points']:.1f}")
    else:
        print(f"\n{person}: No Jira data found")

# Save detailed results to JSON
import json

# Convert Counter objects to dicts for JSON serialization
json_results = {}
for person, data in all_results.items():
    json_results[person] = {}
    for board, metrics in data.items():
        json_results[person][board] = {
            **metrics,
            'issue_types': dict(metrics['issue_types']),
            'statuses': dict(metrics['statuses']),
            'priorities': dict(metrics['priorities'])
        }

with open('../../results/2025/payment/jira_po_analysis_detailed.json', 'w') as f:
    json.dump(json_results, f, indent=2)

print(f"\n✅ Detailed results saved to results/2025/payment/jira_po_analysis_detailed.json")
print("=" * 100)
