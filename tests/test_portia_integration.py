#!/usr/bin/env python3
"""
Test script to demonstrate real Portia API integration in the workflow
"""

import os
import json
from backend.services.portia_service import portia_service

def test_portia_integration():
    """Test real Portia API integration functionality"""
    
    print("🔮 TESTING REAL PORTIA API INTEGRATION")
    print("=" * 50)
    
    # Set up environment with real Portia API key
    os.environ['GITHUB_TOKEN'] = 'your_github_token_here'
os.environ['PORTIA_API_KEY'] = 'your_portia_api_key_here'
    
    # Test issue
    issue_url = "https://github.com/ritik-prog/n8n-automation-templates-5000/issues/5"
    repo = "ritik-prog/n8n-automation-templates-5000"
    
    print(f"📋 Testing Real Portia API with:")
    print(f"   Issue URL: {issue_url}")
    print(f"   Repository: {repo}")
    print(f"   Portia API Key: {os.environ['PORTIA_API_KEY'][:10]}...")
    print()
    
    # Create Portia plan using real API
    print("🔮 Creating Portia plan with real API...")
    portia_plan = portia_service.create_portia_plan(issue_url, repo)
    
    if portia_plan.get('status') == 'fallback':
        print("⚠️  Portia API not available, using fallback")
        return
    
    print("✅ Real Portia API plan created successfully!")
    print()
    
    # Display Portia plan results
    print("🔮 REAL PORTIA API PLAN RESULTS:")
    print("-" * 30)
    
    print(f"Plan ID: {portia_plan.get('portia_plan_id', 'N/A')}")
    print(f"Status: {portia_plan.get('status', 'N/A')}")
    print()
    
    # Portia features used
    features = portia_plan.get('portia_features_used', [])
    print("🔮 Real Portia API Features Used:")
    for feature in features:
        print(f"  ✓ {feature}")
    print()
    
    # Portia plan details
    portia_plan_data = portia_plan.get('portia_plan', {})
    if portia_plan_data:
        print("🧠 REAL PORTIA API PLAN:")
        print("-" * 20)
        
        if portia_plan_data.get('status') == 'success':
            plan_content = portia_plan_data.get('plan', 'No plan content')
            print(f"Plan Content: {plan_content[:500]}...")
            
            run_id = portia_plan_data.get('plan_run_id')
            if run_id:
                print(f"Portia Run ID: {run_id}")
        else:
            print(f"Error: {portia_plan_data.get('error', 'Unknown error')}")
    
    print()
    print("🎉 Real Portia API integration test completed!")
    return portia_plan

if __name__ == "__main__":
    test_portia_integration()
