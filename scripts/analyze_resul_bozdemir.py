#!/usr/bin/env python3
"""
Comprehensive Analysis for Resul Bozdemir
GitLab + Jira Combined Analysis
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

# Load environment
load_dotenv()

# Run GitLab analysis
print("="*100)
print("RESUL BOZDEMİR - COMPREHENSIVE PERFORMANCE ANALYSIS 2025")
print("="*100)
print("\n🔍 Step 1: Fetching GitLab Metrics...")
print("-"*100)

# Call gitlab_user_metrics.py for Resul
gitlab_url = os.getenv('GITLAB_URL', 'https://git.ode.al')
token = os.getenv('GITLAB_TOKEN')

if not token:
    print("❌ GITLAB_TOKEN not found in .env file")
    sys.exit(1)

from gitlab_user_metrics import find_user_metrics

# Analyze for 2025
find_user_metrics(
    gitlab_url=gitlab_url,
    token=token,
    username="resul",  # Will match "Resul Bozdemir" or variations
    start_date="2025-01-01",
    end_date="2025-12-31"
)

print("\n" + "="*100)
print("✅ GitLab analysis complete")
print("="*100)
