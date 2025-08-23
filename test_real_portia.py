#!/usr/bin/env python3
"""
Simple test script to verify real Portia API integration
"""

import os
import sys
import requests
import json

def test_portia_api():
    """Test the real Portia API directly"""
    
    print("🔮 Testing Real Portia API")
    print("=" * 30)
    
    # Portia API configuration
    api_key = "your_portia_api_key_here"
    base_url = "https://api.portialabs.ai"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Simple test query
    test_query = """
    Analyze this simple issue and provide a brief solution:
    
    Issue: The login button is not working properly
    Repository: example/web-app
    
    Please provide:
    1. Brief analysis of the issue
    2. Suggested solution approach
    3. Files that might need modification
    """
    
    run_data = {
        "query": test_query,
        "model": "portia-1",
        "tools": ["code_analysis", "risk_assessment"]
    }
    
    try:
        print(f"🔑 Using Portia API key: {api_key[:10]}...")
        print(f"🌐 API URL: {base_url}/v1/runs")
        print()
        
        print("📤 Sending request to Portia API...")
        response = requests.post(
            f"{base_url}/v1/runs",
            headers=headers,
            json=run_data,
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Portia API call successful!")
            print()
            print("📋 Response:")
            print(f"Run ID: {result.get('id', 'N/A')}")
            print(f"Status: {result.get('status', 'N/A')}")
            
            output = result.get('output', 'No output')
            print(f"Output: {output[:300]}...")
            
            return True
        else:
            print(f"❌ Portia API call failed!")
            print(f"Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return False

def test_portia_integration():
    """Test the Portia integration in our service"""
    
    print("\n🔮 Testing Portia Integration Service")
    print("=" * 40)
    
    try:
        # Set environment variable
        os.environ['PORTIA_API_KEY'] = "your_portia_api_key_here"
        
        # Import and test the service
        from backend.services.portia_service import portia_service
        
        print("✅ Portia service imported successfully")
        print(f"🔑 Service API key: {portia_service.api_key[:10] if portia_service.api_key else 'None'}...")
        print(f"🔧 Service enabled: {portia_service.portia_enabled}")
        
        if portia_service.portia_enabled:
            print("✅ Portia service is enabled and ready!")
            return True
        else:
            print("❌ Portia service is disabled")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Portia integration: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Real Portia API Tests")
    print("=" * 40)
    
    # Test 1: Direct API call
    api_success = test_portia_api()
    
    # Test 2: Integration service
    integration_success = test_portia_integration()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"Direct API Call: {'✅ PASS' if api_success else '❌ FAIL'}")
    print(f"Integration Service: {'✅ PASS' if integration_success else '❌ FAIL'}")
    
    if api_success and integration_success:
        print("\n🎉 All tests passed! Real Portia API integration is working!")
    else:
        print("\n⚠️  Some tests failed. Check the configuration.")
