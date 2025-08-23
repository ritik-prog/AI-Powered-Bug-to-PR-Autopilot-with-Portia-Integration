#!/usr/bin/env python3
"""
AI-Powered Bug-to-PR Autopilot Test
Demonstrates OpenAI-powered intelligent fix generation
"""

import os
import requests
import json
import time
from datetime import datetime

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
REPO = "ritik-prog/n8n-automation-templates-5000"
ISSUE_URL = "https://github.com/ritik-prog/n8n-automation-templates-5000/issues/1"
BACKEND_URL = "http://localhost:8000"

def print_banner():
    """Print test banner"""
    print("""
🤖 AI-POWERED BUG-TO-PR AUTOPILOT TEST
======================================
Testing OpenAI-powered intelligent fix generation
Repository: ritik-prog/n8n-automation-templates-5000
Issue: #1 - Add CONTRIBUTING.md
""")

def check_ai_setup():
    """Check if AI setup is properly configured"""
    print("🔍 Checking AI Setup...")
    
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY not found in environment")
        print("   Set it with: export OPENAI_API_KEY=your_openai_api_key_here")
        return False
    
    print(f"✅ OpenAI API key found: {OPENAI_API_KEY[:10]}...")
    
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN not found in environment")
        return False
    
    print(f"✅ GitHub token found: {GITHUB_TOKEN[:10]}...")
    
    return True

def test_ai_fix_generation():
    """Test AI-powered fix generation directly"""
    print("\n🧪 Testing AI Fix Generation...")
    
    # Test issue data
    issue_data = {
        'title': 'Add CONTRIBUTING.md with guidelines for submitting templates and PR workflow',
        'body': 'Currently, the repository does not include a CONTRIBUTING.md file. Adding one would provide clear, standardized instructions for contributors who want to add new n8n automation templates, fix issues, or improve documentation.',
        'repo': REPO,
        'issue_number': '1',
        'labels': ['documentation', 'enhancement']
    }
    
    try:
        # Import and test AI fix generator
        from backend.services.ai_fix_generator import ai_fix_generator
        
        print("   🔄 Generating AI-powered fix...")
        ai_fix = ai_fix_generator.analyze_issue_and_generate_fix(issue_data, REPO)
        
        print("   ✅ AI fix generation completed!")
        print(f"   📝 Fix type: {ai_fix.get('fix_type', 'unknown')}")
        print(f"   📁 Files to create: {len(ai_fix.get('files', []))}")
        
        # Show AI analysis if available
        if 'ai_analysis' in ai_fix:
            analysis = ai_fix['ai_analysis']
            print(f"   🤖 AI Analysis:")
            print(f"      Issue Type: {analysis.get('issue_type', 'unknown')}")
            print(f"      Priority: {analysis.get('priority', 'unknown')}")
            print(f"      Complexity: {analysis.get('estimated_complexity', 'unknown')}")
        
        # Show generated files
        for file_info in ai_fix.get('files', []):
            print(f"   📄 File: {file_info['path']}")
            print(f"      Message: {file_info['message']}")
            content_preview = file_info['content'][:100] + "..." if len(file_info['content']) > 100 else file_info['content']
            print(f"      Preview: {content_preview}")
        
        return ai_fix
        
    except Exception as e:
        print(f"   ❌ AI fix generation failed: {e}")
        return None

def create_ai_powered_run():
    """Create a run with AI-powered fix generation"""
    print(f"\n🚀 Creating AI-Powered Run...")
    print(f"   Issue URL: {ISSUE_URL}")
    print(f"   Repository: {REPO}")
    
    payload = {
        "issueUrl": ISSUE_URL,
        "repo": REPO
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/runs", json=payload)
        response.raise_for_status()
        run_data = response.json()
        run_id = run_data['runId']
        print(f"   ✅ AI-powered run created with ID: {run_id}")
        return run_id
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Failed to create AI-powered run: {e}")
        return None

def monitor_ai_run(run_id):
    """Monitor the AI-powered run"""
    print(f"\n📊 Monitoring AI-Powered Run...")
    start_time = time.time()
    max_wait_time = 120  # 2 minutes timeout
    
    while time.time() - start_time < max_wait_time:
        run_data = get_run_status(run_id)
        if not run_data:
            time.sleep(2)
            continue
        
        status = run_data.get('status', 'unknown')
        plan = run_data.get('plan', [])
        
        print(f"   ⏱️  Status: {status}")
        
        # Check for waiting gates and approve them
        waiting_gates = [step for step in plan if step.get('status') == 'waiting']
        
        if waiting_gates:
            for step in waiting_gates:
                step_name = step.get('name')
                if step_name in ['propose-fix', 'merge-pr']:
                    print(f"   ⏳ Found waiting gate: {step_name}")
                    approve_gate(run_id, step_name, "AI-powered test approval")
        
        # Check if run is completed
        if status in ['completed', 'failed']:
            print(f"   🎉 Run {status.upper()}!")
            return run_data
        
        time.sleep(3)
    
    print(f"   ⏰ Timeout reached")
    return get_run_status(run_id)

def get_run_status(run_id):
    """Get the current status of a run"""
    try:
        response = requests.get(f"{BACKEND_URL}/runs/{run_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get run status: {e}")
        return None

def approve_gate(run_id, gate, note="AI test approval"):
    """Approve a gate"""
    payload = {
        "gate": gate,
        "decision": "approve",
        "note": note
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/runs/{run_id}/approve", json=payload)
        response.raise_for_status()
        print(f"   ✅ Gate {gate} approved")
        return True
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Failed to approve gate: {e}")
        return False

def display_ai_results(run_data):
    """Display AI-powered run results"""
    print(f"\n🎯 AI-POWERED RUN RESULTS")
    print("=" * 50)
    
    # Basic info
    print(f"Run ID: {run_data.get('runId', 'N/A')}")
    print(f"Status: {run_data.get('status', 'N/A')}")
    print(f"Issue URL: {run_data.get('issueUrl', 'N/A')}")
    print(f"Repository: {run_data.get('repo', 'N/A')}")
    
    # GitHub integration results
    github_data = run_data.get('github_data', {})
    if github_data:
        print(f"\n🔗 GitHub Integration Results:")
        
        if github_data.get('branch'):
            print(f"   Branch Created: {github_data['branch']}")
        
        if github_data.get('pr_url'):
            print(f"   Pull Request: {github_data['pr_url']}")
        
        if github_data.get('pr_number'):
            print(f"   PR Number: #{github_data['pr_number']}")
        
        if github_data.get('pr_title'):
            print(f"   PR Title: {github_data['pr_title']}")
        
        # Show AI analysis
        if github_data.get('ai_analysis'):
            ai_analysis = github_data['ai_analysis']
            print(f"\n🤖 AI Analysis Results:")
            print(f"   Issue Type: {ai_analysis.get('issue_type', 'N/A')}")
            print(f"   Priority: {ai_analysis.get('priority', 'N/A')}")
            print(f"   Complexity: {ai_analysis.get('estimated_complexity', 'N/A')}")
            print(f"   Required Actions: {', '.join(ai_analysis.get('required_actions', []))}")
            print(f"   Technical Requirements: {', '.join(ai_analysis.get('technical_requirements', []))}")
    
    # Plan steps
    print(f"\n📝 Workflow Steps:")
    for i, step in enumerate(run_data.get('plan', []), 1):
        status_icon = {
            'success': '✅',
            'failed': '❌',
            'running': '🔄',
            'waiting': '⏳',
            'pending': '⏸️',
            'cancelled': '🚫'
        }.get(step.get('status'), '❓')
        
        print(f"   {i}. {status_icon} {step.get('name', 'unknown')}: {step.get('status', 'unknown')}")

def verify_ai_github_changes():
    """Verify the AI-generated changes in GitHub"""
    print(f"\n🔍 Verifying AI-Generated GitHub Changes...")
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Check for recent branches
    try:
        response = requests.get(f'https://api.github.com/repos/{REPO}/branches', headers=headers)
        if response.status_code == 200:
            branches = response.json()
            recent_branches = [b for b in branches if 'bugfix' in b['name']]
            if recent_branches:
                print(f"✅ Found recent AI-generated branches:")
                for branch in recent_branches[:3]:  # Show last 3
                    print(f"   - {branch['name']}")
            else:
                print(f"ℹ️  No recent bugfix branches found")
    except Exception as e:
        print(f"❌ Error checking branches: {e}")
    
    # Check for recent PRs
    try:
        response = requests.get(f'https://api.github.com/repos/{REPO}/pulls?state=open', headers=headers)
        if response.status_code == 200:
            prs = response.json()
            if prs:
                print(f"✅ Found open AI-generated pull requests:")
                for pr in prs[:3]:  # Show last 3
                    print(f"   - #{pr['number']}: {pr['title']}")
                    print(f"     URL: {pr['html_url']}")
                    # Check if it's AI-generated by looking at the body
                    if 'AI' in pr.get('body', ''):
                        print(f"     🤖 AI-Generated: Yes")
            else:
                print(f"ℹ️  No open pull requests found")
    except Exception as e:
        print(f"❌ Error checking PRs: {e}")

def main():
    """Main test function"""
    print_banner()
    
    # Check AI setup
    if not check_ai_setup():
        print("❌ AI setup incomplete. Please configure OpenAI API key.")
        return
    
    # Test AI fix generation
    ai_fix = test_ai_fix_generation()
    if not ai_fix:
        print("❌ AI fix generation test failed.")
        return
    
    # Create and monitor AI-powered run
    run_id = create_ai_powered_run()
    if not run_id:
        print("❌ Failed to create AI-powered run.")
        return
    
    # Monitor the run
    run_data = monitor_ai_run(run_id)
    if not run_data:
        print("❌ Failed to complete AI-powered run.")
        return
    
    # Display results
    display_ai_results(run_data)
    
    # Verify GitHub changes
    verify_ai_github_changes()
    
    # Final summary
    print(f"\n🎉 AI-POWERED BUG-TO-PR AUTOPILOT TEST COMPLETED!")
    print("=" * 60)
    
    if run_data.get('status') == 'completed':
        print(f"✅ AI-powered GitHub integration is working!")
        print(f"✅ OpenAI analyzed the issue and generated intelligent solutions")
        print(f"✅ AI-created files and PRs are available in your repository")
        
        github_data = run_data.get('github_data', {})
        if github_data.get('pr_url'):
            print(f"\n🔗 View your AI-generated PR: {github_data['pr_url']}")
        
        if github_data.get('ai_analysis'):
            print(f"\n🤖 AI Analysis Summary:")
            analysis = github_data['ai_analysis']
            print(f"   - Issue Type: {analysis.get('issue_type')}")
            print(f"   - Priority: {analysis.get('priority')}")
            print(f"   - Complexity: {analysis.get('estimated_complexity')}")
    else:
        print(f"⚠️  Test completed but run status was: {run_data.get('status')}")

if __name__ == "__main__":
    main()
