"""
Repository Analyzer Service
Analyzes GitHub repositories to understand project structure, existing files, and codebase patterns
before generating AI-powered fixes.
"""

import os
import requests
import json
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

class RepoAnalyzer:
    """Analyzes GitHub repositories for better AI fix generation"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def analyze_repository(self, repo_name: str) -> Dict[str, Any]:
        """Comprehensive repository analysis"""
        try:
            print(f"🔍 Analyzing repository: {repo_name}")
            
            analysis = {
                'repo_name': repo_name,
                'structure': {},
                'files': {},
                'languages': {},
                'topics': [],
                'readme': None,
                'config_files': {},
                'patterns': {},
                'dependencies': {},
                'summary': {}
            }
            
            # Get repository info
            repo_info = self._get_repo_info(repo_name)
            if repo_info:
                analysis['repo_info'] = repo_info
            
            # Analyze repository structure
            analysis['structure'] = self._analyze_structure(repo_name)
            
            # Get repository languages
            analysis['languages'] = self._get_languages(repo_name)
            
            # Get repository topics
            analysis['topics'] = self._get_topics(repo_name)
            
            # Analyze README and documentation
            analysis['readme'] = self._analyze_readme(repo_name)
            
            # Find configuration files
            analysis['config_files'] = self._find_config_files(repo_name)
            
            # Analyze code patterns
            analysis['patterns'] = self._analyze_patterns(repo_name)
            
            # Find dependencies
            analysis['dependencies'] = self._find_dependencies(repo_name)
            
            # Generate summary
            analysis['summary'] = self._generate_summary(analysis)
            
            print(f"✅ Repository analysis completed for {repo_name}")
            return analysis
            
        except Exception as e:
            print(f"❌ Repository analysis failed: {e}")
            return {
                'repo_name': repo_name,
                'error': str(e),
                'structure': {},
                'files': {},
                'languages': {},
                'topics': [],
                'readme': None,
                'config_files': {},
                'patterns': {},
                'dependencies': {},
                'summary': {}
            }
    
    def _get_repo_info(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Get basic repository information"""
        try:
            url = f"https://api.github.com/repos/{repo_name}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error getting repo info: {e}")
            return None
    
    def _analyze_structure(self, repo_name: str) -> Dict[str, Any]:
        """Analyze repository file structure"""
        try:
            structure = {
                'root_files': [],
                'directories': [],
                'file_count': 0,
                'directory_count': 0,
                'max_depth': 0
            }
            
            # Get root contents
            url = f"https://api.github.com/repos/{repo_name}/contents"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                contents = response.json()
                
                for item in contents:
                    if item['type'] == 'file':
                        structure['root_files'].append({
                            'name': item['name'],
                            'path': item['path'],
                            'size': item['size']
                        })
                        structure['file_count'] += 1
                    elif item['type'] == 'dir':
                        structure['directories'].append({
                            'name': item['name'],
                            'path': item['path']
                        })
                        structure['directory_count'] += 1
                        
                        # Analyze subdirectories (limited depth for performance)
                        sub_structure = self._analyze_subdirectory(repo_name, item['path'], depth=1)
                        structure['directories'][-1]['sub_structure'] = sub_structure
            
            return structure
            
        except Exception as e:
            print(f"Error analyzing structure: {e}")
            return {'error': str(e)}
    
    def _analyze_subdirectory(self, repo_name: str, path: str, depth: int, max_depth: int = 3) -> Dict[str, Any]:
        """Analyze subdirectory structure"""
        if depth > max_depth:
            return {'max_depth_reached': True}
        
        try:
            structure = {
                'files': [],
                'directories': [],
                'depth': depth
            }
            
            url = f"https://api.github.com/repos/{repo_name}/contents/{path}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                contents = response.json()
                
                for item in contents:
                    if item['type'] == 'file':
                        structure['files'].append({
                            'name': item['name'],
                            'path': item['path'],
                            'size': item['size']
                        })
                    elif item['type'] == 'dir':
                        structure['directories'].append({
                            'name': item['name'],
                            'path': item['path']
                        })
            
            return structure
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_languages(self, repo_name: str) -> Dict[str, Any]:
        """Get repository programming languages"""
        try:
            url = f"https://api.github.com/repos/{repo_name}/languages"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                languages = response.json()
                total_bytes = sum(languages.values())
                
                # Calculate percentages
                language_percentages = {}
                for lang, bytes_count in languages.items():
                    percentage = (bytes_count / total_bytes) * 100
                    language_percentages[lang] = {
                        'bytes': bytes_count,
                        'percentage': round(percentage, 2)
                    }
                
                return {
                    'languages': language_percentages,
                    'primary_language': max(languages.items(), key=lambda x: x[1])[0] if languages else None,
                    'total_bytes': total_bytes
                }
            
            return {}
            
        except Exception as e:
            print(f"Error getting languages: {e}")
            return {}
    
    def _get_topics(self, repo_name: str) -> List[str]:
        """Get repository topics"""
        try:
            url = f"https://api.github.com/repos/{repo_name}/topics"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('names', [])
            
            return []
            
        except Exception as e:
            print(f"Error getting topics: {e}")
            return []
    
    def _analyze_readme(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Analyze README and documentation files"""
        try:
            readme_files = ['README.md', 'README.rst', 'README.txt', 'readme.md']
            
            for readme_file in readme_files:
                url = f"https://api.github.com/repos/{repo_name}/contents/{readme_file}"
                response = requests.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    content = response.json()
                    
                    # Get README content
                    content_url = content['download_url']
                    content_response = requests.get(content_url)
                    
                    if content_response.status_code == 200:
                        readme_content = content_response.text
                        
                        return {
                            'file': readme_file,
                            'size': content['size'],
                            'content_preview': readme_content[:1000],  # First 1000 chars
                            'sections': self._extract_readme_sections(readme_content),
                            'has_installation': 'install' in readme_content.lower(),
                            'has_usage': 'usage' in readme_content.lower() or 'example' in readme_content.lower(),
                            'has_contributing': 'contributing' in readme_content.lower(),
                            'has_license': 'license' in readme_content.lower()
                        }
            
            return None
            
        except Exception as e:
            print(f"Error analyzing README: {e}")
            return None
    
    def _extract_readme_sections(self, content: str) -> List[str]:
        """Extract section headers from README"""
        sections = []
        lines = content.split('\n')
        
        for line in lines:
            if line.startswith('#'):
                sections.append(line.strip())
        
        return sections[:10]  # Limit to first 10 sections
    
    def _find_config_files(self, repo_name: str) -> Dict[str, Any]:
        """Find configuration files in the repository"""
        try:
            config_files = {
                'package_managers': [],
                'build_tools': [],
                'linters': [],
                'testing': [],
                'deployment': [],
                'other': []
            }
            
            # Common configuration files
            config_patterns = {
                'package_managers': ['package.json', 'requirements.txt', 'Pipfile', 'pyproject.toml', 'Cargo.toml', 'go.mod'],
                'build_tools': ['Makefile', 'CMakeLists.txt', 'build.gradle', 'pom.xml', 'webpack.config.js'],
                'linters': ['.eslintrc', '.pylintrc', '.flake8', 'tsconfig.json'],
                'testing': ['jest.config.js', 'pytest.ini', '.coveragerc', 'tox.ini'],
                'deployment': ['Dockerfile', 'docker-compose.yml', '.github/workflows', 'deploy.yml'],
                'other': ['.gitignore', '.env.example', 'LICENSE', 'CHANGELOG.md']
            }
            
            # Check for config files in root
            url = f"https://api.github.com/repos/{repo_name}/contents"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                contents = response.json()
                
                for item in contents:
                    if item['type'] == 'file':
                        file_name = item['name']
                        
                        for category, patterns in config_patterns.items():
                            if any(pattern in file_name for pattern in patterns):
                                config_files[category].append({
                                    'name': file_name,
                                    'path': item['path'],
                                    'size': item['size']
                                })
                                break
            
            return config_files
            
        except Exception as e:
            print(f"Error finding config files: {e}")
            return {}
    
    def _analyze_patterns(self, repo_name: str) -> Dict[str, Any]:
        """Analyze code patterns and conventions"""
        try:
            patterns = {
                'naming_conventions': {},
                'file_extensions': {},
                'directory_structure': {},
                'code_style': {}
            }
            
            # Analyze file extensions
            url = f"https://api.github.com/repos/{repo_name}/contents"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                contents = response.json()
                
                extensions = {}
                for item in contents:
                    if item['type'] == 'file':
                        ext = os.path.splitext(item['name'])[1]
                        if ext:
                            extensions[ext] = extensions.get(ext, 0) + 1
                
                patterns['file_extensions'] = extensions
            
            return patterns
            
        except Exception as e:
            print(f"Error analyzing patterns: {e}")
            return {}
    
    def _find_dependencies(self, repo_name: str) -> Dict[str, Any]:
        """Find project dependencies"""
        try:
            dependencies = {
                'package.json': None,
                'requirements.txt': None,
                'other': []
            }
            
            # Check for package.json
            try:
                url = f"https://api.github.com/repos/{repo_name}/contents/package.json"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    content = response.json()
                    content_url = content['download_url']
                    content_response = requests.get(content_url)
                    if content_response.status_code == 200:
                        package_json = json.loads(content_response.text)
                        dependencies['package.json'] = {
                            'dependencies': package_json.get('dependencies', {}),
                            'devDependencies': package_json.get('devDependencies', {}),
                            'scripts': package_json.get('scripts', {})
                        }
            except Exception as e:
                print(f"Error parsing package.json: {e}")
            
            # Check for requirements.txt
            try:
                url = f"https://api.github.com/repos/{repo_name}/contents/requirements.txt"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    content = response.json()
                    content_url = content['download_url']
                    content_response = requests.get(content_url)
                    if content_response.status_code == 200:
                        requirements = content_response.text.split('\n')
                        dependencies['requirements.txt'] = [req.strip() for req in requirements if req.strip()]
            except Exception as e:
                print(f"Error parsing requirements.txt: {e}")
            
            return dependencies
            
        except Exception as e:
            print(f"Error finding dependencies: {e}")
            return {}
    
    def _generate_summary(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the repository analysis"""
        try:
            summary = {
                'project_type': self._determine_project_type(analysis),
                'tech_stack': self._extract_tech_stack(analysis),
                'structure_insights': self._extract_structure_insights(analysis),
                'recommendations': self._generate_recommendations(analysis)
            }
            
            return summary
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return {}
    
    def _determine_project_type(self, analysis: Dict[str, Any]) -> str:
        """Determine the type of project based on analysis"""
        languages = analysis.get('languages', {}).get('languages', {})
        topics = analysis.get('topics', [])
        config_files = analysis.get('config_files', {})
        
        if 'JavaScript' in languages or 'TypeScript' in languages:
            if any('react' in topic.lower() for topic in topics):
                return 'React Application'
            elif any('node' in topic.lower() for topic in topics):
                return 'Node.js Application'
            else:
                return 'JavaScript/TypeScript Project'
        
        elif 'Python' in languages:
            if any('django' in topic.lower() for topic in topics):
                return 'Django Application'
            elif any('flask' in topic.lower() for topic in topics):
                return 'Flask Application'
            else:
                return 'Python Project'
        
        elif 'Java' in languages:
            return 'Java Project'
        
        elif 'Go' in languages:
            return 'Go Project'
        
        elif 'Rust' in languages:
            return 'Rust Project'
        
        else:
            return 'General Software Project'
    
    def _extract_tech_stack(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract the technology stack from analysis"""
        tech_stack = []
        
        # Add languages
        languages = analysis.get('languages', {}).get('languages', {})
        for lang in languages.keys():
            tech_stack.append(lang)
        
        # Add frameworks based on topics
        topics = analysis.get('topics', [])
        for topic in topics:
            if topic.lower() in ['react', 'vue', 'angular', 'django', 'flask', 'express', 'spring']:
                tech_stack.append(topic)
        
        # Add tools based on config files
        config_files = analysis.get('config_files', {})
        if config_files.get('package_managers'):
            tech_stack.append('npm/yarn')
        if config_files.get('build_tools'):
            tech_stack.append('Build Tools')
        if config_files.get('testing'):
            tech_stack.append('Testing Framework')
        
        return list(set(tech_stack))  # Remove duplicates
    
    def _extract_structure_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract insights about the project structure"""
        insights = []
        structure = analysis.get('structure', {})
        
        if structure.get('file_count', 0) > 100:
            insights.append("Large project with many files")
        elif structure.get('file_count', 0) < 10:
            insights.append("Small project with few files")
        
        if structure.get('directory_count', 0) > 5:
            insights.append("Well-organized directory structure")
        
        if analysis.get('readme'):
            insights.append("Has comprehensive documentation")
        else:
            insights.append("Missing or minimal documentation")
        
        return insights
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if not analysis.get('readme'):
            recommendations.append("Add a comprehensive README.md file")
        
        config_files = analysis.get('config_files', {})
        if not config_files.get('testing'):
            recommendations.append("Consider adding testing configuration")
        
        if not config_files.get('linters'):
            recommendations.append("Consider adding code linting configuration")
        
        return recommendations

# Global instance
repo_analyzer = RepoAnalyzer()
