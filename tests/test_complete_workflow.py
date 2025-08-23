#!/usr/bin/env python3
"""
Complete Workflow Test
=====================

This test file calls all backend routes and tests the entire workflow
to ensure everything is working properly and PRs are being created.
"""

import os
import time
from backend.services.github import github_service
from backend.services.ai_fix_generator import AIFixGenerator

# Set environment variables
os.environ['GITHUB_TOKEN'] = 'your_github_token_here'
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key_here'

print('=== Testing Complete Workflow ===')

# 1. Get issue details
issue_details = github_service.get_issue_details('https://github.com/ritik-prog/n8n-automation-templates-5000/issues/9')
print('1. Issue title:', issue_details.get('title'))

# 2. Generate AI fix
ai_generator = AIFixGenerator()
ai_result = ai_generator.analyze_issue_and_generate_fix(issue_details, 'ritik-prog/n8n-automation-templates-5000')
print('2. AI PR title:', ai_result.get('pr_title'))

# Check file content
if ai_result.get('files'):
    for file_info in ai_result['files']:
        content = file_info.get('content', '')
        print('3. File content preview:', repr(content[:100]))
        print('   Content length:', len(content))

# 4. Create branch
timestamp = int(time.time())
branch_name = f'bugfix/auto-fix-{timestamp}'
branch_result = github_service.create_branch('ritik-prog/n8n-automation-templates-5000', 'main', branch_name)
print('4. Branch created:', branch_result.get('success'))

# 5. Create files
if ai_result.get('files'):
    for file_info in ai_result['files']:
        file_result = github_service.create_file(
            'ritik-prog/n8n-automation-templates-5000',
            branch_name,
            file_info['path'],
            file_info['content'],
            file_info['message']
        )
        print('5. File created:', file_result.get('success'))

# 6. Create PR with AI content
pr_result = github_service.create_pull_request(
    'ritik-prog/n8n-automation-templates-5000',
    branch_name,
    'main',
    ai_result.get('pr_title', 'Auto-generated PR'),
    ai_result.get('pr_body', 'Auto-generated PR body')
)

print('6. PR creation result:', pr_result.get('success'))
if pr_result.get('success'):
    print('   PR URL:', pr_result.get('pr_url'))
    print('   PR Number:', pr_result.get('pr_number'))
else:
    print('   Error:', pr_result.get('error'))
