import os
import requests
import base64
import time
from typing import Dict, Any, Optional
from datetime import datetime
from .ai_fix_generator import ai_fix_generator

class GitHubService:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.api_base = 'https://api.github.com'
        self.demo_mode = not self.token or self.token == 'mock_token_for_testing'
        
        if self.demo_mode:
            print("🔧 Running in DEMO MODE - GitHub operations will be simulated")
            self.headers = {}
        else:
            self.headers = {
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            }
    
    def create_branch(self, repo: str, base_branch: str = 'main', new_branch: str = None) -> Dict[str, Any]:
        """Create a new branch from the base branch"""
        if not new_branch:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_branch = f'bugfix/auto-fix-{timestamp}'
        
        if self.demo_mode:
            # Simulate branch creation in demo mode
            return {
                'success': True,
                'branch': new_branch,
                'sha': 'demo_sha_123456',
                'demo_mode': True
            }
        
        # Get the latest commit SHA from base branch
        ref_url = f"{self.api_base}/repos/{repo}/git/ref/heads/{base_branch}"
        response = requests.get(ref_url, headers=self.headers)
        
        if response.status_code != 200:
            return {'error': f'Failed to get base branch: {response.status_code}'}
        
        base_sha = response.json()['object']['sha']
        
        # Create new branch
        create_ref_url = f"{self.api_base}/repos/{repo}/git/refs"
        ref_data = {
            'ref': f'refs/heads/{new_branch}',
            'sha': base_sha
        }
        
        response = requests.post(create_ref_url, headers=self.headers, json=ref_data)
        
        if response.status_code == 201:
            return {
                'success': True,
                'branch': new_branch,
                'sha': base_sha
            }
        else:
            return {'error': f'Failed to create branch: {response.status_code}'}
    
    def create_file(self, repo: str, branch: str, path: str, content: str, message: str) -> Dict[str, Any]:
        """Create or update a file in the repository"""
        if self.demo_mode:
            # Simulate file creation in demo mode
            return {
                'success': True,
                'file': path,
                'sha': 'demo_file_sha_123456',
                'demo_mode': True
            }
        
        url = f"{self.api_base}/repos/{repo}/contents/{path}"
        
        # Check if file exists
        response = requests.get(url, headers=self.headers, params={'ref': branch})
        sha = None
        if response.status_code == 200:
            sha = response.json()['sha']
        
        data = {
            'message': message,
            'content': base64.b64encode(content.encode()).decode(),
            'branch': branch
        }
        
        if sha:
            data['sha'] = sha
        
        response = requests.put(url, headers=self.headers, json=data)
        
        if response.status_code in [201, 200]:
            return {
                'success': True,
                'file': path,
                'sha': response.json()['content']['sha']
            }
        else:
            return {'error': f'Failed to create file: {response.status_code}'}
    
    def create_pull_request(self, repo: str, base_branch: str, head_branch: str, title: str, body: str) -> Dict[str, Any]:
        """Create a pull request"""
        if self.demo_mode:
            # Simulate PR creation in demo mode
            demo_pr_number = int(time.time()) % 1000
            demo_pr_url = f"https://github.com/{repo}/pull/{demo_pr_number}"
            return {
                'success': True,
                'pr_number': demo_pr_number,
                'pr_url': demo_pr_url,
                'pr_title': title,
                'demo_mode': True
            }
        
        # Add a small delay to ensure file commits are processed
        time.sleep(2)
        
        url = f"{self.api_base}/repos/{repo}/pulls"
        
        data = {
            'title': title,
            'body': body,
            'head': head_branch,
            'base': base_branch
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            pr_data = response.json()
            return {
                'success': True,
                'pr_number': pr_data['number'],
                'pr_url': pr_data['html_url'],
                'pr_title': pr_data['title']
            }
        elif response.status_code == 422:
            # Check if PR already exists
            error_data = response.json()
            if 'errors' in error_data:
                for error in error_data['errors']:
                    if 'already exists' in error.get('message', ''):
                        # Try to find the existing PR
                        existing_prs = requests.get(url.replace('/pulls', '/pulls'), headers=self.headers, params={'head': f'{repo.split("/")[0]}:{head_branch}'})
                        if existing_prs.status_code == 200:
                            prs = existing_prs.json()
                            if prs:
                                existing_pr = prs[0]
                                return {
                                    'success': True,
                                    'pr_number': existing_pr['number'],
                                    'pr_url': existing_pr['html_url'],
                                    'pr_title': existing_pr['title'],
                                    'already_exists': True
                                }
            
            return {'error': f'Failed to create PR: {response.status_code} - {error_data.get("message", "Unknown error")}'}
        else:
            return {'error': f'Failed to create PR: {response.status_code}'}
    
    def get_issue_details(self, issue_url: str) -> Dict[str, Any]:
        """Extract issue details from GitHub URL"""
        # Parse issue URL: https://github.com/owner/repo/issues/123
        parts = issue_url.split('/')
        if len(parts) < 7 or parts[2] != 'github.com':
            return {'error': 'Invalid GitHub issue URL'}
        
        owner = parts[3]
        repo = parts[4]
        issue_number = parts[6]
        
        if self.demo_mode:
            # Return demo issue details for the n8n repository
            if repo == 'n8n-automation-templates-5000' and issue_number == '1':
                return {
                    'success': True,
                    'title': 'Add CONTRIBUTING.md with guidelines for submitting templates and PR workflow',
                    'body': 'Currently, the repository does not include a CONTRIBUTING.md file. Adding one would provide clear, standardized instructions for contributors who want to add new n8n automation templates, fix issues, or improve documentation.',
                    'repo': f"{owner}/{repo}",
                    'issue_number': issue_number,
                    'labels': ['documentation', 'enhancement'],
                    'demo_mode': True
                }
            else:
                return {
                    'success': True,
                    'title': f'Demo Issue #{issue_number}',
                    'body': 'This is a demo issue for testing purposes.',
                    'repo': f"{owner}/{repo}",
                    'issue_number': issue_number,
                    'labels': ['demo'],
                    'demo_mode': True
                }
        
        url = f"{self.api_base}/repos/{owner}/{repo}/issues/{issue_number}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            issue_data = response.json()
            return {
                'success': True,
                'title': issue_data['title'],
                'body': issue_data['body'],
                'repo': f"{owner}/{repo}",
                'issue_number': issue_number,
                'labels': [label['name'] for label in issue_data.get('labels', [])]
            }
        else:
            return {'error': f'Failed to get issue: {response.status_code}'}
    
    def create_issue_comment(self, repo: str, issue_number: str, comment: str) -> Dict[str, Any]:
        """Add a comment to an issue"""
        url = f"{self.api_base}/repos/{repo}/issues/{issue_number}/comments"
        
        data = {
            'body': comment
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            return {
                'success': True,
                'comment_id': response.json()['id']
            }
        else:
            return {'error': f'Failed to create comment: {response.status_code}'}

# Global instance
github_service = GitHubService()
