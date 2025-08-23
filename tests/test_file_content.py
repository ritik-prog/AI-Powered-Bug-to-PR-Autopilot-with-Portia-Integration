import os
from backend.services.github import github_service
from backend.services.ai_fix_generator import AIFixGenerator

# Set environment variables
os.environ['GITHUB_TOKEN'] = 'your_github_token_here'
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key_here'

print('Testing AI file content generation...')

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
        print('3. File content preview:')
        print(repr(content[:200]))
        print('Content starts with ```:', content.startswith('```'))
        print('Content length:', len(content))
else:
    print('No files generated')
