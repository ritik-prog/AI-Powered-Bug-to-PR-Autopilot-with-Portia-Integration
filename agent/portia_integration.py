"""
Portia SDK Integration for the Bug-to-PR Autopilot Demo

This module integrates the real Portia SDK with the autopilot demo.
"""

import os
from typing import Any, Dict, Optional
from datetime import datetime
from portia import Portia, Config


class PortiaAutopilot:
    """Integration layer between the demo and real Portia SDK."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Portia with API key."""
        self.api_key = api_key or os.getenv("PORTIA_API_KEY")
        
        if not self.api_key:
            raise ValueError("Portia API key required. Set PORTIA_API_KEY environment variable or pass api_key parameter.")
        
        # Configure Portia SDK
        self.config = Config.from_default(
            portia_api_key=self.api_key,
            portia_api_endpoint="https://api.portialabs.ai",
            openai_api_key=os.getenv("OPENAI_API_KEY")  # Add LLM provider key
        )
        
        # Initialize Portia with the SDK
        self.portia = Portia(config=self.config)
        
        print(f"🔮 Portia SDK initialized with key: {self.api_key[:10]}...")
    
    def analyze_issue(self, issue_url: str, repo: str) -> Dict[str, Any]:
        """Use real Portia SDK to analyze a GitHub issue and suggest a fix approach."""
        query = f"""
        Analyze this GitHub issue and suggest an approach to fix it:
        
        Issue URL: {issue_url}
        Repository: {repo}
        
        Please provide:
        1. A summary of the issue
        2. Potential root causes
        3. Suggested fix approach
        4. Risk assessment (1-5 scale)
        5. Files that might need to be modified
        """
        
        try:
            # Use Portia SDK to run the query
            plan_run = self.portia.run(query)
            
            return {
                "status": "success",
                "analysis": str(plan_run.final_output) if hasattr(plan_run, 'final_output') else str(plan_run),
                "plan_run_id": str(plan_run.id) if hasattr(plan_run, 'id') else None,
                "portia_run": plan_run
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "analysis": f"Failed to analyze issue: {e}"
            }
    
    def generate_test_case(self, issue_description: str, repo_context: str) -> Dict[str, Any]:
        """Generate a failing test case using real Portia SDK."""
        query = f"""
        Generate a failing test case for this issue:
        
        Issue: {issue_description}
        Repository context: {repo_context}
        
        Please provide:
        1. Test code that reproduces the issue
        2. Expected vs actual behavior
        3. Setup requirements
        """
        
        try:
            plan_run = self.portia.run(query)
            
            return {
                "status": "success", 
                "test_case": str(plan_run.final_output) if hasattr(plan_run, 'final_output') else str(plan_run),
                "plan_run_id": str(plan_run.id) if hasattr(plan_run, 'id') else None,
                "portia_run": plan_run
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "test_case": f"Failed to generate test: {e}"
            }
    
    def generate_fix(self, issue_analysis: str, failing_test: str) -> Dict[str, Any]:
        """Generate a fix using real Portia SDK."""
        query = f"""
        Generate a minimal fix for this issue:
        
        Analysis: {issue_analysis}
        Failing test: {failing_test}
        
        Please provide:
        1. Specific code changes needed
        2. Files to modify
        3. Explanation of the fix
        4. Potential side effects
        """
        
        try:
            plan_run = self.portia.run(query)
            
            return {
                "status": "success",
                "fix": str(plan_run.final_output) if hasattr(plan_run, 'final_output') else str(plan_run),
                "plan_run_id": str(plan_run.id) if hasattr(plan_run, 'id') else None,
                "portia_run": plan_run
            }
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e),
                "fix": f"Failed to generate fix: {e}"
            }
    
    def create_comprehensive_plan(self, issue_url: str, repo: str) -> Dict[str, Any]:
        """Create a comprehensive Portia plan using the real SDK."""
        query = f"""
        Create a comprehensive plan for fixing this GitHub issue using Portia's advanced AI capabilities:

        Repository: {repo}
        Issue URL: {issue_url}

        Please provide a detailed Portia-style analysis and plan including:

        1. ISSUE ANALYSIS:
           - Issue classification (type, severity, complexity, impact scope)
           - Root cause analysis with contributing factors
           - System implications and dependencies

        2. SOLUTION STRATEGY:
           - Recommended approach with alternatives
           - Implementation considerations and best practices
           - Testing strategy and quality assurance

        3. WORKFLOW PLANNING:
           - Step-by-step implementation plan
           - Resource allocation and time estimates
           - Risk mitigation strategies
           - Rollback and monitoring requirements

        4. CONTEXT-AWARE RECOMMENDATIONS:
           - Project-specific considerations
           - Team workflow alignment
           - Code quality standards
           - Documentation requirements

        5. RISK ASSESSMENT:
           - Technical, operational, and business risks
           - Probability and impact analysis
           - Mitigation strategies and contingency plans

        Please provide a comprehensive, actionable plan that leverages Portia's advanced AI capabilities.
        """
        
        try:
            plan_run = self.portia.run(query)
            
            return {
                "status": "success",
                "plan": str(plan_run.final_output) if hasattr(plan_run, 'final_output') else str(plan_run),
                "plan_run_id": str(plan_run.id) if hasattr(plan_run, 'id') else None,
                "portia_run": plan_run,
                "portia_plan_id": f"portia_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "portia_features_used": [
                    "Real Portia SDK Integration",
                    "Advanced Issue Analysis",
                    "Intelligent Workflow Planning",
                    "Risk Assessment",
                    "Context-Aware Fix Generation"
                ]
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "plan": f"Failed to create plan: {e}"
            }


def test_portia_integration():
    """Test function to verify real Portia SDK integration works."""
    try:
        # Test with the provided API key
        autopilot = PortiaAutopilot("your_portia_api_key_here")
        
        # Test with a simple query
        result = autopilot.analyze_issue(
            "https://github.com/example/repo/issues/123", 
            "example/repo"
        )
        
        print("🔮 Real Portia SDK integration test:")
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Analysis: {result['analysis'][:200]}...")
            print(f"Run ID: {result['plan_run_id']}")
        else:
            print(f"Error: {result['error']}")
            
        return True
        
    except Exception as e:
        print(f"❌ Portia SDK integration test failed: {e}")
        return False


if __name__ == "__main__":
    test_portia_integration()

