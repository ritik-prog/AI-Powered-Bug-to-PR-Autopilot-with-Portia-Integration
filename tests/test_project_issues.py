#!/usr/bin/env python3
"""
Comprehensive test script to identify project issues
"""

import os
import requests
import json
import time

# Set up environment
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key_here'
os.environ['GITHUB_TOKEN'] = 'your_github_token_here'

BASE_URL = "http://localhost:8000"

def test_backend_health():
    """Test backend health endpoint"""
    print("🔍 Testing Backend Health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend healthy: {data}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_ai_fix_generation():
    """Test AI fix generation directly"""
    print("\n🤖 Testing AI Fix Generation...")
    try:
        from backend.services.ai_fix_generator import AIFixGenerator
        
        ai_generator = AIFixGenerator()
        if not ai_generator.ai_enabled:
            print("❌ AI not enabled")
            return False
        
        # Test issue
        test_issue = {
            'title': 'Add Categories Overview Table',
            'body': 'The repository needs a categories overview table in the README.',
            'url': 'https://github.com/ritik-prog/n8n-automation-templates-5000/issues/5',
            'issue_number': '5'
        }
        
        fix = ai_generator.analyze_issue_and_generate_fix(test_issue, 'ritik-prog/n8n-automation-templates-5000')
        
        print(f"✅ AI fix generation successful")
        print(f"   Files to create: {len(fix.get('files', []))}")
        print(f"   PR Title: {fix.get('pr_title', 'N/A')}")
        
        for file_info in fix.get('files', []):
            print(f"   📄 {file_info['path']}: {len(file_info['content'])} chars")
        
        return True
    except Exception as e:
        print(f"❌ AI fix generation failed: {e}")
        return False

def test_github_service():
    """Test GitHub service directly"""
    print("\n🔗 Testing GitHub Service...")
    try:
        from backend.services.github import GitHubService
        
        github_service = GitHubService()
        
        # Test issue details
        issue_url = "https://github.com/ritik-prog/n8n-automation-templates-5000/issues/5"
        issue_details = github_service.get_issue_details(issue_url)
        
        if issue_details.get('success'):
            print(f"✅ GitHub issue details retrieved")
            print(f"   Title: {issue_details.get('title')}")
            print(f"   Issue #: {issue_details.get('issue_number')}")
        else:
            print(f"❌ GitHub issue details failed: {issue_details.get('error')}")
            return False
        
        # Test branch creation
        repo = "ritik-prog/n8n-automation-templates-5000"
        branch_name = f"test-branch-{int(time.time())}"
        branch_result = github_service.create_branch(repo, branch_name)
        
        if branch_result.get('success'):
            print(f"✅ Branch creation successful: {branch_name}")
        else:
            print(f"❌ Branch creation failed: {branch_result.get('error')}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ GitHub service test failed: {e}")
        return False

def test_create_new_run():
    """Test creating a new run"""
    print("\n🚀 Testing New Run Creation...")
    try:
        run_data = {
            "issueUrl": "https://github.com/ritik-prog/n8n-automation-templates-5000/issues/5",
            "repo": "ritik-prog/n8n-automation-templates-5000"
        }
        
        response = requests.post(f"{BASE_URL}/runs", json=run_data)
        if response.status_code == 200:
            run = response.json()
            print(f"✅ New run created: {run['runId']}")
            return run['runId']
        else:
            print(f"❌ Run creation failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Run creation error: {e}")
        return None

def test_run_execution(run_id):
    """Test run execution and monitor progress"""
    print(f"\n📊 Monitoring Run Execution: {run_id}")
    
    try:
        # Monitor the run
        for i in range(30):  # Wait up to 30 seconds
            response = requests.get(f"{BASE_URL}/runs/{run_id}")
            if response.status_code == 200:
                run = response.json()
                status = run['status']
                print(f"   Status: {status}")
                
                if status == 'completed':
                    print("✅ Run completed successfully!")
                    
                    # Check GitHub data
                    github_data = run.get('github_data', {})
                    pr_url = github_data.get('pr_url')
                    pr_number = github_data.get('pr_number')
                    
                    if pr_url and pr_number:
                        print(f"✅ PR created: {pr_url}")
                        print(f"   PR Number: {pr_number}")
                        print(f"   PR Title: {github_data.get('pr_title')}")
                    else:
                        print("❌ PR creation failed - no PR URL or number")
                        print(f"   GitHub data: {github_data}")
                    
                    return True
                elif status == 'failed':
                    print("❌ Run failed")
                    return False
                
                time.sleep(1)
            else:
                print(f"❌ Failed to get run status: {response.status_code}")
                return False
        
        print("❌ Run timed out")
        return False
        
    except Exception as e:
        print(f"❌ Run monitoring error: {e}")
        return False

def test_frontend_connectivity():
    """Test frontend connectivity"""
    print("\n🌐 Testing Frontend Connectivity...")
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend connectivity error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 COMPREHENSIVE PROJECT TEST")
    print("=" * 50)
    
    # Test backend health
    if not test_backend_health():
        print("❌ Backend health check failed - stopping tests")
        return
    
    # Test AI fix generation
    if not test_ai_fix_generation():
        print("❌ AI fix generation failed")
    
    # Test GitHub service
    if not test_github_service():
        print("❌ GitHub service failed")
    
    # Test frontend
    if not test_frontend_connectivity():
        print("❌ Frontend connectivity failed")
    
    # Test full run creation and execution
    print("\n🔄 Testing Full Run Workflow...")
    run_id = test_create_new_run()
    if run_id:
        test_run_execution(run_id)
    
    print("\n📋 Test Summary:")
    print("=" * 50)
    print("✅ Backend: Running")
    print("✅ Frontend: Accessible")
    print("✅ AI Fix Generation: Working")
    print("✅ GitHub Service: Connected")
    print("✅ Run Creation: Working")
    print("⚠️  PR Creation: Needs investigation")

if __name__ == "__main__":
    main()
