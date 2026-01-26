#!/usr/bin/env python3
"""
GitLab Project Discovery Tool
Lists all groups and projects to help configure DORA metrics collection
"""

import os
import sys
from dotenv import load_dotenv
import gitlab
from tabulate import tabulate


def discover_gitlab_resources(gitlab_url: str, token: str):
    """Discover all accessible groups and projects in GitLab"""

    gl = gitlab.Gitlab(gitlab_url, private_token=token)

    try:
        # Authenticate
        gl.auth()
        current_user = gl.user
        print(f"\n✓ Connected to GitLab as: {current_user.name} (@{current_user.username})")
        print(f"  GitLab URL: {gitlab_url}")
        print("="*80)

    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\nPlease check:")
        print("1. GITLAB_URL is correct")
        print("2. GITLAB_TOKEN has 'api' or 'read_api' scope")
        sys.exit(1)

    # Discover Groups
    print("\n" + "="*80)
    print("📁 AVAILABLE GROUPS")
    print("="*80)

    try:
        groups = gl.groups.list(all=True, order_by='name')

        if groups:
            group_data = []
            for group in groups:
                group_data.append([
                    group.id,
                    group.name,
                    group.full_path,
                    group.web_url
                ])

            print(tabulate(
                group_data,
                headers=['Group ID', 'Name', 'Full Path', 'URL'],
                tablefmt='grid'
            ))

            print(f"\n📊 Total Groups: {len(groups)}")

            # Show how to use group ID
            if groups:
                print(f"\n💡 To collect metrics for a group, use:")
                print(f"   GROUP_ID={groups[0].id}")
                print(f"   # This will automatically include all projects in '{groups[0].name}'")

        else:
            print("No groups found or you don't have access to any groups")

    except Exception as e:
        print(f"❌ Error fetching groups: {e}")

    # Discover Projects
    print("\n" + "="*80)
    print("📦 AVAILABLE PROJECTS")
    print("="*80)

    try:
        # Get projects accessible to the user
        projects = gl.projects.list(
            all=True,
            order_by='name',
            membership=True  # Only projects user is member of
        )

        if projects:
            project_data = []
            for project in projects:
                # Get group name if project belongs to a group
                namespace = project.namespace.get('name', 'Personal')

                project_data.append([
                    project.id,
                    project.name,
                    namespace,
                    project.default_branch if hasattr(project, 'default_branch') else 'N/A',
                    project.web_url
                ])

            print(tabulate(
                project_data,
                headers=['Project ID', 'Name', 'Group/Namespace', 'Default Branch', 'URL'],
                tablefmt='grid'
            ))

            print(f"\n📊 Total Projects: {len(projects)}")

            # Generate PROJECT_IDS configuration
            project_ids = [str(p.id) for p in projects[:10]]  # First 10 as example
            print(f"\n💡 Example configuration for first {min(10, len(projects))} projects:")
            print(f"   PROJECT_IDS={','.join(project_ids)}")

            if len(projects) > 10:
                print(f"   # ... and {len(projects) - 10} more projects")

        else:
            print("No projects found or you don't have access to any projects")

    except Exception as e:
        print(f"❌ Error fetching projects: {e}")

    # Discover Projects by Group
    if groups:
        print("\n" + "="*80)
        print("📂 PROJECTS BY GROUP")
        print("="*80)

        for group in groups[:5]:  # Show first 5 groups
            try:
                group_obj = gl.groups.get(group.id)
                group_projects = group_obj.projects.list(all=True)

                if group_projects:
                    print(f"\n🏷️  Group: {group.name} (ID: {group.id})")
                    print(f"   Projects: {len(group_projects)}")

                    for proj in group_projects[:5]:  # Show first 5 projects
                        print(f"   • {proj.name} (ID: {proj.id})")

                    if len(group_projects) > 5:
                        print(f"   ... and {len(group_projects) - 5} more projects")

                    print(f"\n   💡 Use this to collect all projects in this group:")
                    print(f"      GROUP_ID={group.id}")

            except Exception as e:
                print(f"   ❌ Could not fetch projects for group {group.name}: {e}")

        if len(groups) > 5:
            print(f"\n   ... and {len(groups) - 5} more groups")

    # Summary and recommendations
    print("\n" + "="*80)
    print("📋 CONFIGURATION RECOMMENDATIONS")
    print("="*80)

    print("\n✅ Option 1: Use a GROUP_ID (Recommended for team metrics)")
    print("   - Automatically includes all projects in the group")
    print("   - Easier to maintain as projects are added/removed")
    if groups:
        print(f"   - Example: GROUP_ID={groups[0].id}  # {groups[0].name}")

    print("\n✅ Option 2: Use specific PROJECT_IDS")
    print("   - Cherry-pick specific projects")
    print("   - More control over which projects to analyze")
    if projects and len(projects) > 0:
        example_ids = ','.join([str(p.id) for p in projects[:3]])
        print(f"   - Example: PROJECT_IDS={example_ids}")

    print("\n✅ Option 3: Use multiple groups")
    print("   - You can modify the script to accept multiple GROUP_IDs")
    print("   - Or run the script separately for each group")

    print("\n" + "="*80)


def main():
    load_dotenv()

    gitlab_url = os.getenv('GITLAB_URL')
    gitlab_token = os.getenv('GITLAB_TOKEN')

    if not gitlab_url or not gitlab_token:
        print("❌ Error: GITLAB_URL and GITLAB_TOKEN must be set in .env file")
        print("\nPlease:")
        print("1. Copy .env.example to .env")
        print("2. Fill in your GitLab URL and Personal Access Token")
        sys.exit(1)

    discover_gitlab_resources(gitlab_url, gitlab_token)

    print("\n🎉 Discovery complete!")
    print("\nNext steps:")
    print("1. Update your .env file with the GROUP_ID or PROJECT_IDS from above")
    print("2. Run: python3 gitlab_dora_metrics.py")
    print()


if __name__ == '__main__':
    main()
