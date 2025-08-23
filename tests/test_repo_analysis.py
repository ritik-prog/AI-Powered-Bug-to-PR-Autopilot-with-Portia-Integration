#!/usr/bin/env python3
"""
Test script to demonstrate repository analysis feature
"""

import os
import json
from backend.services.repo_analyzer import repo_analyzer
from backend.services.ai_fix_generator import AIFixGenerator

def test_repository_analysis():
    """Test repository analysis functionality"""
    
    print("🔍 TESTING REPOSITORY ANALYSIS FEATURE")
    print("=" * 50)
    
    # Set up environment
    os.environ['GITHUB_TOKEN'] = 'your_github_token_here'
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key_here'
    
    # Test repository
    repo_name = "ritik-prog/n8n-automation-templates-5000"
    
    print(f"📋 Analyzing repository: {repo_name}")
    print()
    
    # Analyze repository
    analysis = repo_analyzer.analyze_repository(repo_name)
    
    if 'error' in analysis:
        print(f"❌ Repository analysis failed: {analysis['error']}")
        return
    
    print("✅ Repository analysis completed!")
    print()
    
    # Display analysis results
    print("📊 ANALYSIS RESULTS:")
    print("-" * 30)
    
    # Project summary
    summary = analysis.get('summary', {})
    print(f"Project Type: {summary.get('project_type', 'Unknown')}")
    print(f"Tech Stack: {', '.join(summary.get('tech_stack', []))}")
    print()
    
    # Structure
    structure = analysis.get('structure', {})
    print(f"File Count: {structure.get('file_count', 0)}")
    print(f"Directory Count: {structure.get('directory_count', 0)}")
    
    if structure.get('directories'):
        print("Main Directories:")
        for dir_info in structure['directories']:
            print(f"  - {dir_info['name']}")
    print()
    
    # Languages
    languages = analysis.get('languages', {})
    if languages.get('languages'):
        print("Languages:")
        for lang, info in languages['languages'].items():
            print(f"  - {lang}: {info['percentage']}%")
        print(f"Primary Language: {languages.get('primary_language', 'Unknown')}")
    print()
    
    # Topics
    topics = analysis.get('topics', [])
    if topics:
        print(f"Repository Topics: {', '.join(topics)}")
        print()
    
    # README
    readme = analysis.get('readme')
    if readme:
        print(f"README: {readme['file']} ({readme['size']} bytes)")
        if readme.get('has_installation'):
            print("  ✓ Has installation instructions")
        if readme.get('has_usage'):
            print("  ✓ Has usage examples")
        if readme.get('has_contributing'):
            print("  ✓ Has contributing guidelines")
    else:
        print("README: Not found")
    print()
    
    # Configuration files
    config_files = analysis.get('config_files', {})
    if config_files.get('package_managers'):
        print("Package Manager Files:")
        for file_info in config_files['package_managers']:
            print(f"  - {file_info['name']}")
    print()
    
    # Structure insights
    insights = summary.get('structure_insights', [])
    if insights:
        print("Structure Insights:")
        for insight in insights:
            print(f"  - {insight}")
    print()
    
    # Recommendations
    recommendations = summary.get('recommendations', [])
    if recommendations:
        print("Recommendations:")
        for rec in recommendations:
            print(f"  - {rec}")
    print()
    
    # Test AI fix generation with repository context
    print("🤖 TESTING AI FIX GENERATION WITH REPOSITORY CONTEXT")
    print("-" * 50)
    
    ai_generator = AIFixGenerator()
    if not ai_generator.ai_enabled:
        print("❌ AI not enabled")
        return
    
    # Test issue
    test_issue = {
        'title': 'Add Categories Overview Table',
        'body': 'The repository needs a categories overview table in the README.',
        'url': 'https://github.com/ritik-prog/n8n-automation-templates-5000/issues/5',
        'issue_number': '5'
    }
    
    print(f"📋 Test Issue: {test_issue['title']}")
    print()
    
    # Generate AI fix with repository context
    fix = ai_generator.analyze_issue_and_generate_fix(test_issue, repo_name)
    
    print("✅ AI fix generation with repository context completed!")
    print()
    
    # Display fix results
    print("📝 FIX RESULTS:")
    print("-" * 20)
    
    print(f"Fix Type: {fix.get('fix_type', 'unknown')}")
    print(f"Files to Create: {len(fix.get('files', []))}")
    print(f"PR Title: {fix.get('pr_title', 'N/A')}")
    print()
    
    # Show generated files
    for file_info in fix.get('files', []):
        print(f"📄 File: {file_info['path']}")
        print(f"   Message: {file_info['message']}")
        print(f"   Content Length: {len(file_info['content'])} characters")
        print(f"   Content Preview: {file_info['content'][:200]}...")
        print()
    
    # Show AI analysis
    if 'ai_analysis' in fix:
        ai_analysis = fix['ai_analysis']
        print("🤖 AI ANALYSIS:")
        print("-" * 15)
        print(f"Issue Type: {ai_analysis.get('issue_type', 'unknown')}")
        print(f"Priority: {ai_analysis.get('priority', 'unknown')}")
        print(f"Complexity: {ai_analysis.get('estimated_complexity', 'unknown')}")
        print(f"Files to Create: {ai_analysis.get('files_to_create', [])}")
        print(f"Required Actions: {ai_analysis.get('required_actions', [])}")
        print()
    
    print("🎉 Repository analysis feature test completed!")

if __name__ == "__main__":
    test_repository_analysis()
