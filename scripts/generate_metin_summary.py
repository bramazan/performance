#!/usr/bin/env python3
"""Generate summary insights for Metin İsfendiyar report"""

import pandas as pd
import numpy as np

# Read the combined analysis
df = pd.read_excel('jira-analysis/metin_isfendiyar_combined_analysis.xlsx')

print("="*100)
print("METIN İSFENDİYAR - ADDITIONAL INSIGHTS")
print("="*100)
print()

# Find best and worst stories by detail quality
stories = df[df['type'] == 'Story'].copy()

print(f"📝 STORY ANALYSIS (Total: {len(stories)} stories)")
print()

# Story detail quality
story_avg_detail = stories['detail_score'].mean()
story_avg_words = stories['description_words'].mean()
story_avg_comments = stories['comment_count'].mean()

print(f"Story Quality Metrics:")
print(f"   Average Detail Score: {story_avg_detail:.1f}/100")
print(f"   Average Description: {story_avg_words:.0f} words")
print(f"   Average Comments: {story_avg_comments:.1f}")
print()

# Best stories
print("🌟 Top 5 Stories by Detail:")
top_stories = stories.nlargest(5, 'detail_score')[['key', 'summary', 'detail_score', 'description_words', 'comment_count', 'status']]
for idx, row in top_stories.iterrows():
    print(f"   {row['key']:12s} | {row['detail_score']:>5.1f} | {row['description_words']:>3}w | {row['comment_count']:>2}c | {row['status']:15s}")
    print(f"                └─ {row['summary'][:70]}")
print()

# Worst stories
print("⚠️  Bottom 5 Stories by Detail:")
bottom_stories = stories.nsmallest(5, 'detail_score')[['key', 'summary', 'detail_score', 'description_words', 'comment_count', 'status']]
for idx, row in bottom_stories.iterrows():
    print(f"   {row['key']:12s} | {row['detail_score']:>5.1f} | {row['description_words']:>3}w | {row['comment_count']:>2}c | {row['status']:15s}")
    print(f"                └─ {row['summary'][:70]}")
print()

# Status breakdown for stories
print("📊 Story Status Breakdown:")
for status, count in stories['status'].value_counts().items():
    pct = count / len(stories) * 100
    print(f"   • {status:25s}: {count:>4} ({pct:>5.1f}%)")
print()

# Technical Analysis detail
tech_analysis = df[df['type'] == 'Technical Analysis'].copy()
print(f"🔍 TECHNICAL ANALYSIS ISSUES (Total: {len(tech_analysis)})")
print(f"   Average Detail Score: {tech_analysis['detail_score'].mean():.1f}/100")
print(f"   Average Description: {tech_analysis['description_words'].mean():.0f} words")
print()

# Bug analysis
bugs = df[df['type'] == 'Bug'].copy()
print(f"🐛 BUG ANALYSIS (Total: {len(bugs)})")
print(f"   Average Detail Score: {bugs['detail_score'].mean():.1f}/100")
print(f"   Average Description: {bugs['description_words'].mean():.0f} words")
print()

print("Bug Status:")
for status, count in bugs['status'].value_counts().head(5).items():
    pct = count / len(bugs) * 100
    print(f"   • {status:25s}: {count:>4} ({pct:>5.1f}%)")
print()

# Priority vs Detail correlation
print("⚡ PRIORITY vs DETAIL QUALITY CORRELATION")
priority_detail = df.groupby('priority').agg({
    'detail_score': 'mean',
    'key': 'count',
    'description_words': 'mean'
}).rename(columns={'key': 'count', 'description_words': 'avg_words'})

for priority, row in priority_detail.sort_values('detail_score', ascending=False).iterrows():
    print(f"   {priority:15s}: Detail: {row['detail_score']:>5.1f} | Avg Words: {row['avg_words']:>4.0f} | Count: {row['count']:>4}")
print()

# Issues with no description
no_desc = df[df['description_words'] == 0]
print(f"🚨 ISSUES WITH NO DESCRIPTION: {len(no_desc)} ({len(no_desc)/len(df)*100:.1f}%)")
if len(no_desc) > 0:
    print("\nBreakdown by type:")
    for itype, count in no_desc['type'].value_counts().items():
        print(f"   • {itype:20s}: {count:>4}")
print()

# Completion by type
print("✅ COMPLETION RATE BY ISSUE TYPE")
for itype in df['type'].unique():
    type_df = df[df['type'] == itype]
    done_count = (type_df['status'] == 'Done').sum()
    completion = done_count / len(type_df) * 100 if len(type_df) > 0 else 0
    print(f"   • {itype:20s}: {done_count:>4}/{len(type_df):<4} ({completion:>5.1f}%)")
print()

# Weekly distribution (approximation)
df['week'] = df['created'].dt.isocalendar().week
weekly = df.groupby('week').size()

print("📅 WEEKLY DISTRIBUTION (Top 10 weeks)")
for week, count in weekly.nlargest(10).items():
    bar = '█' * min(int(count / 50), 40)
    print(f"   Week {week:>2}: {count:>4} issues {bar}")
print()

print("="*100)
