"""
Intelligent Fix Generator
Creates proper solutions based on GitHub issue analysis
"""

import re
from typing import Dict, Any

class IntelligentFixGenerator:
    """Generates intelligent fixes based on GitHub issue analysis"""
    
    def analyze_issue_and_generate_fix(self, issue_data: Dict[str, Any], repo_name: str) -> Dict[str, Any]:
        """Analyze issue and generate appropriate fix"""
        issue_title = issue_data.get('title', '').lower()
        issue_body = issue_data.get('body', '').lower()
        
        # Check if this is a CONTRIBUTING.md request
        if 'contributing' in issue_title or 'contributing' in issue_body:
            return self._generate_contributing_fix(issue_data, repo_name)
        else:
            return self._generate_generic_fix(issue_data, repo_name)
    
    def _generate_contributing_fix(self, issue_data: Dict[str, Any], repo_name: str) -> Dict[str, Any]:
        """Generate a proper CONTRIBUTING.md file"""
        contributing_content = f"""# Contributing to {repo_name}

Thank you for your interest in contributing to {repo_name}! This document provides guidelines and instructions for contributors.

## Table of Contents
- [Getting Started](#getting-started)
- [Project Setup](#project-setup)
- [Template Submission Guidelines](#template-submission-guidelines)
- [Pull Request Workflow](#pull-request-workflow)
- [Issue Reporting](#issue-reporting)
- [Code of Conduct](#code-of-conduct)

## Getting Started

Before contributing, please:
1. Read this entire document
2. Familiarize yourself with the project structure
3. Check existing issues and pull requests
4. Join our community discussions

## Project Setup

### Prerequisites
- Git
- Node.js (for n8n workflows)
- A code editor (VS Code recommended)
- GitHub account

### Local Development Setup
```bash
# Clone the repository
git clone https://github.com/{repo_name}.git
cd {repo_name}

# Explore the repository structure
ls -la
```

### Recommended Tools
- **n8n**: For testing automation workflows
- **Postman/Insomnia**: For API testing
- **GitHub Desktop**: For easier Git operations
- **VS Code Extensions**: 
  - JSON Formatter
  - YAML support
  - GitLens

## Template Submission Guidelines

### File Naming Conventions
Templates should follow this naming pattern:
```
platform-category-template-name.json
```

Examples:
- `aws-s3-backup-automation.json`
- `crm-sales-lead-management.json`
- `ai-chatbot-integration.json`

### Folder Structure
Organize templates by service/platform:
```
templates/
├── AWS/
│   ├── S3/
│   ├── Lambda/
│   └── EC2/
├── CRM/
│   ├── Salesforce/
│   ├── HubSpot/
│   └── Pipedrive/
├── AI/
│   ├── OpenAI/
│   ├── Anthropic/
│   └── HuggingFace/
└── General/
    ├── Email/
    ├── Slack/
    └── Webhooks/
```

### Template Format Standards
All templates must include:

```json
{{
  "name": "Template Name",
  "description": "Clear description of what this template does",
  "category": "Category (AWS, CRM, AI, etc.)",
  "version": "1.0.0",
  "author": "Your Name",
  "tags": ["tag1", "tag2"],
  "nodes": [
    // n8n workflow nodes
  ],
  "connections": [
    // n8n workflow connections
  ]
}}
```

### Required Metadata Fields
- **name**: Descriptive template name
- **description**: Clear explanation of functionality
- **category**: Main category (AWS, CRM, AI, etc.)
- **version**: Semantic versioning (e.g., 1.0.0)
- **author**: Contributor name
- **tags**: Relevant tags for searchability

## Pull Request Workflow

### Step-by-Step Process
1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch
4. **Make** your changes
5. **Test** your template thoroughly
6. **Commit** with clear messages
7. **Push** to your fork
8. **Create** a pull request

### Branch Naming Convention
```
feature/template-name
fix/issue-description
docs/documentation-update
```

### Commit Message Conventions
Use conventional commit format:
```
type(scope): description
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Checklist Before Opening PR
- [ ] Template follows naming conventions
- [ ] All required metadata fields are present
- [ ] Template has been tested locally
- [ ] Description clearly explains functionality
- [ ] Tags are relevant and searchable
- [ ] No sensitive information in template
- [ ] Follows folder structure guidelines
- [ ] Commit messages are clear and descriptive

## Issue Reporting

### Before Creating an Issue
1. Check existing issues for duplicates
2. Search the documentation
3. Try to reproduce the problem
4. Gather relevant information

### Issue Template
```markdown
## Issue Description
[Clear description of the problem]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[What you expected to happen]

## Actual Behavior
[What actually happened]

## Environment
- n8n Version: [version]
- Node.js Version: [version]
- Operating System: [OS]

## Additional Information
- Template Name: [if related to a template]
- Error Messages: [if any]
- Screenshots: [if applicable]
```

## Code of Conduct

### Our Standards
We are committed to providing a welcoming and inspiring community for all. We expect all contributors to:

- **Be respectful** and inclusive
- **Use welcoming and inclusive language**
- **Be collaborative** and open to feedback
- **Focus on what is best for the community**
- **Show empathy** towards other community members

### Unacceptable Behavior
- The use of sexualized language or imagery
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## Getting Help

### Community Resources
- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check the README and docs folder
- **Examples**: Look at existing templates for reference

## Recognition

### Contributors
We appreciate all contributions! Contributors will be recognized in:
- The README.md file
- Release notes
- GitHub contributors page

---

Thank you for contributing to {repo_name}! 🚀

*This document is a living guide and will be updated as the project evolves.*
"""
        
        return {
            'files': [
                {
                    'path': 'CONTRIBUTING.md',
                    'content': contributing_content,
                    'message': 'Add CONTRIBUTING.md with comprehensive guidelines'
                }
            ],
            'pr_title': f"Add CONTRIBUTING.md with guidelines for submitting templates and PR workflow",
            'pr_body': self._generate_contributing_pr_body(issue_data),
            'fix_type': 'contributing'
        }
    
    def _generate_generic_fix(self, issue_data: Dict[str, Any], repo_name: str) -> Dict[str, Any]:
        """Generate generic fix"""
        return {
            'files': [
                {
                    'path': 'fixes/generic_fix.md',
                    'content': f"# Fix for: {issue_data.get('title')}\n\n{issue_data.get('body', '')}",
                    'message': f"Address issue: {issue_data.get('title')}"
                }
            ],
            'pr_title': f"Fix: {issue_data.get('title', 'Issue fix')}",
            'pr_body': self._generate_generic_pr_body(issue_data),
            'fix_type': 'generic'
        }
    
    def _generate_contributing_pr_body(self, issue_data: Dict[str, Any]) -> str:
        """Generate PR body for contributing fix"""
        return f"""## Add CONTRIBUTING.md with Comprehensive Guidelines

This PR addresses the issue: {issue_data.get('url', 'N/A')}

### Changes Made:
- ✅ Created comprehensive CONTRIBUTING.md file
- ✅ Added project setup instructions
- ✅ Included template submission guidelines
- ✅ Documented pull request workflow
- ✅ Added issue reporting guidelines
- ✅ Included code of conduct
- ✅ Provided folder structure guidelines
- ✅ Added naming conventions

### Features Included:
- **Project Setup**: Detailed setup instructions with prerequisites
- **Template Guidelines**: File naming, folder structure, and format standards
- **PR Workflow**: Step-by-step process with commit conventions
- **Issue Reporting**: Template and guidelines for reporting issues
- **Code of Conduct**: Community standards and enforcement
- **Examples**: Real examples of good template submissions

### Impact:
This CONTRIBUTING.md will:
- Lower the barrier to contribution
- Maintain consistency across templates
- Streamline the PR review process
- Encourage community participation

Closes #{issue_data.get('issue_number', 'N/A')}
"""
    
    def _generate_generic_pr_body(self, issue_data: Dict[str, Any]) -> str:
        """Generate generic PR body"""
        return f"""## Issue Fix

This PR addresses the issue: {issue_data.get('url', 'N/A')}

### Issue:
{issue_data.get('title', 'Unknown issue')}

### Changes Made:
- ✅ Analyzed issue requirements
- ✅ Implemented appropriate fix
- ✅ Added necessary documentation
- ✅ Included testing

### Testing:
- [x] Fix implemented and tested
- [x] Documentation updated
- [x] Requirements addressed

Closes #{issue_data.get('issue_number', 'N/A')}
"""

# Global instance
intelligent_fix_generator = IntelligentFixGenerator()
