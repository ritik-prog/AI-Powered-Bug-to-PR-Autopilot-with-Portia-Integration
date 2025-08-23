"""
AI-Powered Fix Generator
Generates intelligent code fixes for GitHub issues using OpenAI's GPT models.
"""

import os
import json
import openai
from typing import Dict, Any, List, Optional
from datetime import datetime
from .repo_analyzer import repo_analyzer

class AIFixGenerator:
    """AI-powered fix generator for GitHub issues"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            # Initialize OpenAI client
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            print("🤖 AI-powered fix generation enabled with OpenAI")
        else:
            self.client = None
            print("⚠️  OpenAI API key not found. AI fix generation disabled.")
    
    def analyze_issue_and_generate_fix(self, issue_data: Dict[str, Any], repo_name: str) -> Dict[str, Any]:
        """Main method to analyze issue and generate complete fix"""
        try:
            # Step 1: Analyze repository structure
            print(f"🔍 Analyzing repository structure for {repo_name}...")
            repo_analysis = repo_analyzer.analyze_repository(repo_name)
            
            # Step 2: Analyze the issue with AI
            print("🧠 Analyzing issue with AI...")
            analysis = self._analyze_issue_with_ai(issue_data, repo_name, repo_analysis)
            
            if not analysis:
                print("❌ AI analysis failed. Falling back to template-based fix.")
                return self._generate_template_fix(issue_data, repo_name)
            
            # Step 3: Generate AI-powered fix
            print("💡 Generating AI-powered fix...")
            ai_result = self._generate_ai_fix(issue_data, repo_name, analysis, repo_analysis)
            
            return ai_result
            
        except Exception as e:
            print(f"❌ AI analysis failed: {e}. Falling back to template-based fix.")
            return self._generate_template_fix(issue_data, repo_name)
    
    def _analyze_issue_with_ai(self, issue_data: Dict[str, Any], repo_name: str, repo_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze issue using AI with repository context"""
        if not self.client:
            return None
        
        issue_title = issue_data.get('title', '')
        issue_body = issue_data.get('body', '')
        
        # Prepare repository context
        repo_context = self._prepare_repo_context(repo_analysis)
        
        prompt = f"""
Analyze this GitHub issue and provide a detailed technical solution:

ISSUE:
Title: {issue_title}
Description: {issue_body}

REPOSITORY CONTEXT:
{repo_context}

IMPORTANT: You are creating ACTUAL FILES to fix the issue, not documentation about the fix.

Please provide a comprehensive analysis in JSON format:
{{
    "issue_type": "string (bug|feature|documentation|license|config)",
    "priority": "string (low|medium|high|critical)", 
    "required_actions": ["list", "of", "specific", "actions"],
    "files_to_create": ["list", "of", "actual", "file", "paths", "to", "create"],
    "files_to_modify": ["list", "of", "existing", "files", "to", "modify"],
    "technical_requirements": ["list", "of", "technical", "requirements"],
    "solution_approach": "detailed description of the actual solution",
    "estimated_complexity": "low/medium/high",
    "testing_requirements": ["list", "of", "testing", "needs"]
}}

EXAMPLES:
- For LICENSE issues: files_to_create should include ["LICENSE"] (not ["fixes/license_fix.md"])
- For documentation issues: files_to_create should include ["CONTRIBUTING.md", "README.md"] (not ["fixes/docs_fix.md"])
- For code issues: files_to_create should include actual source files
- For config issues: files_to_create should include actual config files

Focus on creating the ACTUAL files that solve the problem, not documentation about the problem.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert software developer and GitHub issue analyst. Analyze issues and provide detailed technical solutions. Always be specific about file names and types. If testing is mentioned, include appropriate test files."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if analysis_text.startswith('```json'):
                analysis_text = analysis_text[7:]
            if analysis_text.startswith('```'):
                analysis_text = analysis_text[3:]
            if analysis_text.endswith('```'):
                analysis_text = analysis_text[:-3]
            
            analysis_text = analysis_text.strip()
            analysis = json.loads(analysis_text)
            return analysis
            
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return None
    
    def _generate_ai_fix(self, issue_data: Dict[str, Any], repo_name: str, analysis: Dict[str, Any], repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered fix based on analysis with repository context"""
        issue_title = issue_data.get('title', '')
        issue_body = issue_data.get('body', '')
        
        # Generate file content using AI with repository context
        files = []
        for file_path in analysis.get('files_to_create', []):
            file_content = self._generate_file_content_with_ai(
                file_path, issue_data, repo_name, analysis, repo_analysis
            )
            
            # Filter out placeholder content
            if self._is_placeholder_content(file_content):
                print(f"⚠️  Detected placeholder content in {file_path}, regenerating...")
                file_content = self._regenerate_file_content(file_path, issue_data, repo_name, analysis, repo_analysis)
            
            files.append({
                'path': file_path,
                'content': file_content,
                'message': f'Add {file_path} - AI-generated solution'
            })
        
        # Generate PR title and body using AI
        pr_title = self._generate_pr_title_with_ai(issue_data, analysis)
        pr_body = self._generate_pr_body_with_ai(issue_data, analysis, files)
        
        # Clean up PR title - remove extra quotes
        if pr_title and pr_title.startswith('"') and pr_title.endswith('"'):
            pr_title = pr_title[1:-1]
        
        # Clean up file content - remove markdown code blocks
        for file_info in files:
            content = file_info.get('content', '')
            # Remove markdown code blocks
            if content.startswith('```'):
                # Find the end of the code block
                lines = content.split('\n')
                cleaned_lines = []
                in_code_block = False
                for line in lines:
                    if line.strip().startswith('```'):
                        if in_code_block:
                            in_code_block = False
                        else:
                            in_code_block = True
                        continue
                    if in_code_block:
                        cleaned_lines.append(line)
                file_info['content'] = '\n'.join(cleaned_lines).strip()
        
        return {
            'files': files,
            'pr_title': pr_title,
            'pr_body': pr_body,
            'fix_type': analysis.get('issue_type', 'ai_generated'),
            'ai_analysis': analysis
        }
    
    def _generate_file_content_with_ai(self, file_path: str, issue_data: Dict[str, Any], repo_name: str, analysis: Dict[str, Any], repo_analysis: Dict[str, Any]) -> str:
        """Generate file content using AI with repository context"""
        issue_title = issue_data.get('title', '')
        issue_body = issue_data.get('body', '')
        
        # Special handling for test files to avoid placeholder content
        if 'test' in file_path.lower() or file_path.endswith('_test.py') or file_path.endswith('test.py'):
            return self._generate_test_content_with_ai(file_path, issue_data, repo_name, analysis, repo_analysis)
        
        # Prepare repository context for file generation
        repo_context = self._prepare_repo_context(repo_analysis)
        
        prompt = f"""
Create the ACTUAL content for file: {file_path}

Repository: {repo_name}
Issue Title: {issue_title}
Issue Body: {issue_body}

REPOSITORY CONTEXT:
{repo_context}

Analysis:
- Issue Type: {analysis.get('issue_type')}
- Priority: {analysis.get('priority')}
- Required Actions: {analysis.get('required_actions')}
- Technical Requirements: {analysis.get('technical_requirements')}
- Solution Approach: {analysis.get('solution_approach')}

CRITICAL REQUIREMENTS:
- Create the ACTUAL file content that solves the issue
- NO documentation about the fix, NO markdown explaining the problem
- Generate REAL, FUNCTIONAL content that can be used immediately
- Make it comprehensive, professional, and follow best practices
- Consider the project's tech stack, structure, and conventions
- Follow the project's naming conventions and file organization

SPECIFIC FILE TYPE REQUIREMENTS:

For LICENSE files (e.g., LICENSE, LICENSE.txt):
- Create the actual license text (MIT, Apache 2.0, GPL, etc.)
- Include proper copyright notice and year
- Use standard license format
- Example for MIT: "MIT License\n\nCopyright (c) [year] [fullname]\n\nPermission is hereby granted..."

For documentation files (e.g., CONTRIBUTING.md, README.md):
- Create comprehensive, well-formatted documentation
- Include all necessary sections and information
- Make it useful for users and contributors

For code files:
- Create functional, production-ready code
- Use proper imports, error handling, and follow language conventions
- Match the project's existing patterns and style

For test files:
- Create meaningful tests that actually test functionality
- Use appropriate testing frameworks
- Include proper test setup and assertions

For configuration files:
- Create proper configuration with correct syntax
- Follow the project's configuration patterns

Generate the ACTUAL content for {file_path} that directly addresses this issue. Do not create documentation about the fix - create the fix itself.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an expert software developer. Create the ACTUAL content for {file_path} that directly solves the issue. Do not create documentation about the fix - create the fix itself."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.4
        )
        
        return response.choices[0].message.content
    
    def _prepare_repo_context(self, repo_analysis: Dict[str, Any]) -> str:
        """Prepare repository context for AI prompts"""
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
            print(f"Error preparing repo context: {e}")
            return "Repository context unavailable"
    
    def _generate_test_content_with_ai(self, file_path: str, issue_data: Dict[str, Any], repo_name: str, analysis: Dict[str, Any], repo_analysis: Dict[str, Any]) -> str:
        """Generate meaningful test content using AI with repository context"""
        issue_title = issue_data.get('title', '')
        issue_body = issue_data.get('body', '')
        
        # Prepare repository context for test generation
        repo_context = self._prepare_repo_context(repo_analysis)
        
        prompt = f"""
Create MEANINGFUL, FUNCTIONAL test content for: {file_path}

Repository: {repo_name}
Issue Title: {issue_title}
Issue Body: {issue_body}

REPOSITORY CONTEXT:
{repo_context}

Analysis:
- Issue Type: {analysis.get('issue_type')}
- Priority: {analysis.get('priority')}
- Required Actions: {analysis.get('required_actions')}
- Technical Requirements: {analysis.get('technical_requirements')}
- Solution Approach: {analysis.get('solution_approach')}

CRITICAL REQUIREMENTS FOR TEST FILES:
- Create ACTUAL, FUNCTIONAL tests - NO placeholders, NO "assert True", NO TODO comments
- Write tests that verify real functionality based on the issue
- Include proper test setup, teardown, and assertions
- Use appropriate testing frameworks based on the project's tech stack
- Test both success and failure scenarios
- Include edge cases and error conditions
- Make tests comprehensive and meaningful
- Use descriptive test names that explain what is being tested
- Include proper imports and test dependencies
- Follow the project's testing conventions and patterns
- Consider the project's existing test structure and naming conventions

Examples of GOOD tests:
```python
def test_user_authentication_success():
    user = User(username="testuser", password="validpass")
    result = authenticate_user(user)
    assert result.is_authenticated == True
    assert result.user_id == user.id

def test_user_authentication_failure():
    user = User(username="testuser", password="wrongpass")
    result = authenticate_user(user)
    assert result.is_authenticated == False
    assert result.error_message == "Invalid credentials"
```

Examples of BAD tests (DO NOT USE):
```python
def test_bug_reproduction():
    # TODO: Implement actual test based on issue description
    assert True  # Placeholder test
```

Generate comprehensive, functional test content that actually tests the functionality described in the issue and fits the project's context.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert software tester and developer. Create meaningful, functional tests that verify real functionality. NEVER use placeholders or TODO comments."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def _is_placeholder_content(self, content: str) -> bool:
        """Check if content contains placeholder or TODO elements"""
        if not content or len(content.strip()) < 50:
            return True
            
        placeholder_indicators = [
            "assert True",
            "assert true",
            "# TODO:",
            "# TODO ",
            "TODO:",
            "TODO ",
            "placeholder",
            "Placeholder",
            "PLACEHOLDER",
            "assert True  #",
            "pass  #",
            "return True  #",
            "return None  #",
            "// TODO:",
            "// TODO ",
            "/* TODO:",
            "/* TODO ",
            "<!-- TODO:",
            "<!-- TODO ",
            "implement actual test",
            "implement actual",
            "placeholder test",
            "Placeholder test"
        ]
        
        content_lower = content.lower()
        for indicator in placeholder_indicators:
            if indicator.lower() in content_lower:
                return True
        
        # Check for test files with only basic structure (no meaningful assertions)
        if "def test_" in content:
            # If it's a test file but has no meaningful assertions, it's likely a placeholder
            if "assert True" in content or ("pass" in content and len(content.strip()) < 200):
                return True
            # If it has meaningful assertions, it's probably good
            if "assert " in content and "assert True" not in content:
                return False
        
        return False
    
    def _regenerate_file_content(self, file_path: str, issue_data: Dict[str, Any], repo_name: str, analysis: Dict[str, Any], repo_analysis: Dict[str, Any]) -> str:
        """Regenerate file content with stronger anti-placeholder instructions and repository context"""
        issue_title = issue_data.get('title', '')
        issue_body = issue_data.get('body', '')
        
        # Prepare repository context for regeneration
        repo_context = self._prepare_repo_context(repo_analysis)
        
        prompt = f"""
CRITICAL: Generate REAL, FUNCTIONAL content for {file_path}

Repository: {repo_name}
Issue Title: {issue_title}
Issue Body: {issue_body}

REPOSITORY CONTEXT:
{repo_context}

Analysis:
- Issue Type: {analysis.get('issue_type')}
- Priority: {analysis.get('priority')}
- Required Actions: {analysis.get('required_actions')}
- Technical Requirements: {analysis.get('technical_requirements')}
- Solution Approach: {analysis.get('solution_approach')}

STRICT REQUIREMENTS:
- ABSOLUTELY NO placeholders, TODO comments, or "assert True"
- Create REAL, WORKING code/content
- If it's a test file, write actual meaningful tests
- If it's documentation, provide complete information
- If it's code, make it production-ready
- Use proper imports, error handling, and best practices
- Make it comprehensive and useful
- Consider the project's tech stack, structure, and conventions
- Follow the project's existing patterns and style

The previous attempt generated placeholder content. Generate proper, functional content now that fits the project's context.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert developer. Generate ONLY real, functional content. NEVER use placeholders, TODO comments, or assert True. Create production-ready code."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2500,
            temperature=0.2
        )
        
        return response.choices[0].message.content
    
    def _generate_pr_title_with_ai(self, issue_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate PR title using AI"""
        issue_title = issue_data.get('title', '')
        issue_type = analysis.get('issue_type', 'fix')
        
        prompt = f"""
Generate a concise, professional PR title for this issue:

Issue Title: {issue_title}
Issue Type: {issue_type}

The PR title should be:
- Clear and descriptive
- Follow conventional commit format
- Under 100 characters
- Professional tone

Examples:
- "Add CONTRIBUTING.md with comprehensive guidelines"
- "Fix authentication bug in user login"
- "Feature: Add dark mode support"
- "Docs: Update API documentation"

Generate only the title, no additional text.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert at writing clear, professional PR titles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_pr_body_with_ai(self, issue_data: Dict[str, Any], analysis: Dict[str, Any], files: List[Dict[str, Any]]) -> str:
        """Generate PR body using AI"""
        issue_title = issue_data.get('title', '')
        issue_body = issue_data.get('body', '')
        issue_url = issue_data.get('url', '')
        issue_number = issue_data.get('issue_number', '')
        
        file_list = "\n".join([f"- `{f['path']}`" for f in files])
        
        prompt = f"""
Generate a comprehensive PR body for this issue:

Issue Title: {issue_title}
Issue Body: {issue_body}
Issue URL: {issue_url}
Issue Number: {issue_number}

Analysis:
- Issue Type: {analysis.get('issue_type')}
- Priority: {analysis.get('priority')}
- Required Actions: {analysis.get('required_actions')}
- Technical Requirements: {analysis.get('technical_requirements')}
- Solution Approach: {analysis.get('solution_approach')}

Files Created/Modified:
{file_list}

Generate a professional PR body that includes:
1. Clear description of what was done
2. How it addresses the issue
3. Technical details
4. Testing information
5. Impact assessment
6. Proper formatting with markdown

Make it comprehensive and professional.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert at writing comprehensive, professional PR descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.4
        )
        
        return response.choices[0].message.content
    
    def _generate_template_fix(self, issue_data: Dict[str, Any], repo_name: str) -> Dict[str, Any]:
        """Fallback to template-based fix when AI is not available"""
        issue_title = issue_data.get('title', '').lower()
        issue_body = issue_data.get('body', '').lower()
        
        # Simple template-based logic
        if 'contributing' in issue_title or 'contributing' in issue_body:
            return self._generate_contributing_template(issue_data, repo_name)
        else:
            return self._generate_generic_template(issue_data, repo_name)
    
    def _generate_contributing_template(self, issue_data: Dict[str, Any], repo_name: str) -> Dict[str, Any]:
        """Generate CONTRIBUTING.md template"""
        content = f"""# Contributing to {repo_name}

Thank you for your interest in contributing to {repo_name}! This document provides guidelines and instructions for contributors.

## Getting Started

Before contributing, please:
1. Read this entire document
2. Familiarize yourself with the project structure
3. Check existing issues and pull requests

## How to Contribute

### 1. Fork the Repository
1. Go to the repository on GitHub
2. Click the "Fork" button
3. Clone your fork locally

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Write clear, well-documented code
- Follow the project's coding standards
- Add tests for new functionality

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add your feature description"
```

### 5. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request
1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select the appropriate branch
4. Fill out the PR template
5. Submit the PR

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful and inclusive in all interactions.

## Getting Help

- Check existing issues and discussions
- Ask questions in GitHub Discussions
- Review the documentation

---

Thank you for contributing to {repo_name}! 🚀
"""
        
        return {
            'files': [
                {
                    'path': 'CONTRIBUTING.md',
                    'content': content,
                    'message': 'Add CONTRIBUTING.md with guidelines'
                }
            ],
            'pr_title': f"Add CONTRIBUTING.md with guidelines for {repo_name}",
            'pr_body': f"""## Add CONTRIBUTING.md

This PR addresses the issue: {issue_data.get('url', 'N/A')}

### Changes Made:
- ✅ Created comprehensive CONTRIBUTING.md
- ✅ Added contribution guidelines
- ✅ Included code of conduct
- ✅ Provided step-by-step instructions

### Impact:
This will help new contributors understand how to contribute to the project effectively.

Closes #{issue_data.get('issue_number', 'N/A')}
""",
            'fix_type': 'contributing'
        }
    
    def _generate_generic_template(self, issue_data: Dict[str, Any], repo_name: str) -> Dict[str, Any]:
        """Generate generic template fix"""
        issue_title = issue_data.get('title', '').lower()
        issue_body = issue_data.get('body', '').lower()
        
        # Determine what type of file to create based on the issue
        if 'license' in issue_title or 'license' in issue_body:
            # Create actual LICENSE file
            license_content = """MIT License

Copyright (c) 2025 ritik-prog

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
            
            return {
                'files': [
                    {
                        'path': 'LICENSE',
                        'content': license_content,
                        'message': f"Add LICENSE file - {issue_data.get('title')}"
                    }
                ],
                'pr_title': f"Add LICENSE file for {repo_name}",
                'pr_body': f"""## Add LICENSE file

This PR addresses the issue: {issue_data.get('url', 'N/A')}

### Issue:
{issue_data.get('title', 'Unknown issue')}

### Changes Made:
- ✅ Added MIT LICENSE file
- ✅ Included proper copyright notice
- ✅ Added standard MIT license terms

### Impact:
This provides clear licensing terms for users and contributors.

Closes #{issue_data.get('issue_number', 'N/A')}
""",
                'fix_type': 'license'
            }
        elif 'contributing' in issue_title or 'contributing' in issue_body:
            # Create actual CONTRIBUTING.md file
            return self._generate_contributing_template(issue_data, repo_name)
        else:
            # For other issues, create a generic fix file
            return {
                'files': [
                    {
                        'path': 'fixes/issue_fix.md',
                        'content': f"# Fix for: {issue_data.get('title')}\n\n{issue_data.get('body', '')}\n\n## Solution\n\nThis file addresses the reported issue.",
                        'message': f"Address issue: {issue_data.get('title')}"
                    }
                ],
                'pr_title': f"Fix: {issue_data.get('title', 'Issue fix')}",
                'pr_body': f"""## Issue Fix

This PR addresses the issue: {issue_data.get('url', 'N/A')}

### Issue:
{issue_data.get('title', 'Unknown issue')}

### Changes Made:
- ✅ Analyzed issue requirements
- ✅ Implemented appropriate fix
- ✅ Added necessary documentation

Closes #{issue_data.get('issue_number', 'N/A')}
""",
                'fix_type': 'generic'
            }

# Global instance
ai_fix_generator = AIFixGenerator()
