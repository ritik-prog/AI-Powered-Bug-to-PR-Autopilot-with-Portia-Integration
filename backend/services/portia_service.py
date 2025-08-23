"""
Portia Service Integration
Integrates real Portia SDK with our current AI-powered system.
"""

import os
import asyncio
import time
import threading
from datetime import datetime
from typing import Dict, Any, Optional
from portia import Portia, Config
from .repo_analyzer import repo_analyzer

class PortiaService:
    """Real Portia SDK service for advanced AI analysis and workflow planning"""
    
    def __init__(self):
        self.portia_enabled = True
        self.api_key = os.getenv("PORTIA_API_KEY")
        self.timeout = 120  # 2 minutes timeout for Portia API calls
        self.running_analyses = {}  # Track running analyses
        
        if not self.api_key:
            print("⚠️  PORTIA_API_KEY not found, falling back to mock service")
            self.portia_enabled = False
            return
        
        try:
            # Initialize Portia SDK with proper configuration
            self.config = Config.from_default(
                portia_api_key=self.api_key,
                portia_api_endpoint="https://api.portialabs.ai",
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            self.portia = Portia(config=self.config)
            print(f"🔮 Real Portia SDK service enabled with key: {self.api_key[:10]}...")
        except Exception as e:
            print(f"❌ Failed to initialize Portia SDK: {e}")
            self.portia_enabled = False
    
    def create_portia_plan(self, issue_url: str, repo: str) -> Dict[str, Any]:
        """Create a real Portia plan for the issue - returns immediately with background processing"""
        if not self.portia_enabled:
            return self._fallback_plan(issue_url, repo)
        
        try:
            # Step 1: Repository Analysis (quick, synchronous)
            print("🔍 Portia: Analyzing repository structure...")
            repo_analysis = repo_analyzer.analyze_repository(repo)
            
            # Step 2: Start Portia analysis in background
            analysis_id = f"portia_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            print(f"🧠 Portia: Starting background analysis with ID: {analysis_id}")
            
            # Start background thread for Portia analysis
            thread = threading.Thread(
                target=self._run_portia_analysis_background,
                args=(analysis_id, issue_url, repo, repo_analysis)
            )
            thread.daemon = True
            thread.start()
            
            # Return immediately with analysis ID
            return {
                "portia_plan_id": analysis_id,
                "status": "processing",
                "repository_analysis": repo_analysis,
                "portia_plan": {
                    "status": "processing",
                    "message": "Portia analysis is running in background",
                    "analysis_id": analysis_id
                },
                "portia_features_used": [
                    "Real Portia SDK Integration",
                    "Repository Structure Analysis",
                    "Advanced Issue Analysis", 
                    "Intelligent Workflow Planning",
                    "Risk Assessment",
                    "Context-Aware Fix Generation"
                ]
            }
            
        except Exception as e:
            print(f"❌ Portia plan creation failed: {e}")
            return self._fallback_plan(issue_url, repo)
    
    def _run_portia_analysis_background(self, analysis_id: str, issue_url: str, repo: str, repo_analysis: Dict[str, Any]):
        """Run Portia analysis in background thread"""
        try:
            print(f"⏱️  Starting Portia analysis {analysis_id} with {self.timeout}s timeout...")
            start_time = time.time()
            
            # Store analysis status
            self.running_analyses[analysis_id] = {
                "status": "running",
                "start_time": start_time,
                "progress": "Initializing..."
            }
            
            # Create comprehensive plan using the real Portia SDK
            portia_plan = self._create_real_portia_plan(issue_url, repo, repo_analysis)
            
            total_time = time.time() - start_time
            print(f"✅ Portia analysis {analysis_id} completed in {total_time:.1f} seconds")
            
            # Update analysis status
            self.running_analyses[analysis_id] = {
                "status": "completed",
                "start_time": start_time,
                "end_time": time.time(),
                "execution_time": total_time,
                "result": portia_plan
            }
            
        except Exception as e:
            print(f"❌ Portia analysis {analysis_id} failed: {e}")
            self.running_analyses[analysis_id] = {
                "status": "failed",
                "error": str(e),
                "start_time": start_time,
                "end_time": time.time()
            }
    
    def get_analysis_status(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a running or completed analysis"""
        return self.running_analyses.get(analysis_id)
    
    def _create_real_portia_plan(self, issue_url: str, repo: str, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive plan using the real Portia SDK with timeout handling"""
        try:
            # Prepare repository context
            repo_context = self._prepare_portia_context(repo_analysis)
            
            query = f"""
Create a comprehensive plan for fixing this GitHub issue using Portia's advanced AI capabilities:

Repository: {repo}
Issue URL: {issue_url}

REPOSITORY CONTEXT:
{repo_context}

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
            
            print(f"⏱️  Starting Portia analysis with {self.timeout}s timeout...")
            start_time = time.time()
            
            # Use Portia SDK to run the query with timeout
            plan_run = self.portia.run(query)
            
            # Wait for completion with timeout
            elapsed_time = 0
            while not hasattr(plan_run, 'final_output') or plan_run.final_output is None:
                if elapsed_time > self.timeout:
                    raise TimeoutError(f"Portia analysis timed out after {self.timeout} seconds")
                
                time.sleep(2)  # Check every 2 seconds
                elapsed_time = time.time() - start_time
                print(f"⏱️  Portia analysis in progress... ({elapsed_time:.1f}s elapsed)")
            
            total_time = time.time() - start_time
            print(f"✅ Portia analysis completed in {total_time:.1f} seconds")
            
            return {
                "status": "success",
                "plan": str(plan_run.final_output) if hasattr(plan_run, 'final_output') else str(plan_run),
                "plan_run_id": str(plan_run.id) if hasattr(plan_run, 'id') else None,
                "portia_run": plan_run,
                "execution_time": total_time
            }
                
        except TimeoutError as e:
            print(f"⏰ Portia analysis timed out: {e}")
            return {
                "status": "timeout",
                "error": str(e),
                "plan": f"Portia analysis timed out after {self.timeout} seconds. Please try again."
            }
        except Exception as e:
            print(f"❌ Error in real Portia plan creation: {e}")
            return {
                "status": "error",
                "error": str(e),
                "plan": f"Failed to create Portia plan: {e}"
            }
    

    
    def _prepare_portia_context(self, repo_analysis: Dict[str, Any]) -> str:
        """Prepare repository context for Portia analysis"""
        try:
            context_parts = []
            
            # Project type and tech stack
            summary = repo_analysis.get('summary', {})
            project_type = summary.get('project_type', 'Unknown')
            tech_stack = summary.get('tech_stack', [])
            
            context_parts.append(f"Project Type: {project_type}")
            if tech_stack:
                context_parts.append(f"Tech Stack: {', '.join(tech_stack)}")
            
            # Repository structure
            structure = repo_analysis.get('structure', {})
            if structure.get('directories'):
                dirs = [d['name'] for d in structure['directories']]
                context_parts.append(f"Main Directories: {', '.join(dirs)}")
            
            # Languages
            languages = repo_analysis.get('languages', {}).get('languages', {})
            if languages:
                primary_lang = repo_analysis.get('languages', {}).get('primary_language', 'Unknown')
                context_parts.append(f"Primary Language: {primary_lang}")
                context_parts.append(f"Languages: {', '.join(languages.keys())}")
            
            # Configuration files
            config_files = repo_analysis.get('config_files', {})
            if config_files.get('package_managers'):
                context_parts.append(f"Package Manager Files: {', '.join([f['name'] for f in config_files['package_managers']])}")
            
            # README analysis
            readme = repo_analysis.get('readme')
            if readme:
                context_parts.append(f"Has README: Yes ({readme['file']})")
                if readme.get('has_installation'):
                    context_parts.append("Has installation instructions")
                if readme.get('has_usage'):
                    context_parts.append("Has usage examples")
                if readme.get('has_contributing'):
                    context_parts.append("Has contributing guidelines")
            else:
                context_parts.append("Has README: No")
            
            # Topics
            topics = repo_analysis.get('topics', [])
            if topics:
                context_parts.append(f"Repository Topics: {', '.join(topics)}")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            print(f"Error preparing Portia context: {e}")
            return "Repository context unavailable"
    
    def _fallback_plan(self, issue_url: str, repo: str) -> Dict[str, Any]:
        """Fallback plan when Portia is not available"""
        return {
            "portia_plan_id": f"fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "fallback",
            "message": "Portia SDK not available, using standard workflow",
            "portia_features_used": ["Standard workflow only"]
        }

# Global instance
portia_service = PortiaService()
