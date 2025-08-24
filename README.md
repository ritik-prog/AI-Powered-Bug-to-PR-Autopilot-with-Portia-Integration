# 🔮 AI-Powered Bug-to-PR Autopilot with Portia Integration

An intelligent automation system that transforms GitHub issues into production-ready pull requests using **Portia AI** for advanced workflow orchestration and **OpenAI** for intelligent content generation.

## 🎯 What It Does

This system automatically:

- **Analyzes GitHub issues** using Portia AI for deep understanding and root cause analysis
- **Generates intelligent fixes** with AI-powered code generation and test case creation
- **Creates professional PRs** with comprehensive documentation and risk assessment
- **Provides human-in-the-loop approval** with detailed workflow management
- **Handles post-deployment verification** with automated health checks

## 🚀 Quick Start

### 1. **One-Command Setup**

```bash
python install_and_run.py
```

This will:

- ✅ Install all dependencies (Python + Node.js)
- ✅ Set up virtual environment
- ✅ Configure environment variables
- ✅ Start backend (port 8000) and frontend (port 3000)

### 2. **Set Up API Keys**

```bash
# Edit the .env file created by the setup script
nano .env

# Add your API keys:
GITHUB_TOKEN=ghp_your_github_token_here
OPENAI_API_KEY=sk-your_openai_api_key_here
PORTIA_API_KEY=your_portia_api_key_here
```

### 3. **Test AI Integration**

```bash
python test_ai_powered.py
```

### 4. **Use the Web Interface**

Open `http://localhost:3000` in your browser and start creating AI-powered PRs!

## 🔑 Required API Keys

### **GitHub Personal Access Token**

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`, `write:packages`
4. Copy the token (starts with `ghp_`)

### **OpenAI API Key**

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### **Portia API Key**

1. Go to [Portia Labs](https://portialabs.ai)
2. Sign up for an account
3. Navigate to API settings
4. Generate your API key

## 🧪 Testing

### **AI-Powered Test**

```bash
python test_ai_powered.py
```

This comprehensive test:

- ✅ Validates API key configuration
- ✅ Tests Portia AI-powered issue analysis
- ✅ Tests OpenAI-powered fix generation
- ✅ Creates real GitHub PRs with AI-generated content
- ✅ Verifies GitHub integration
- ✅ Shows detailed results and analysis

### **Manual Testing**

1. Open `http://localhost:3000`
2. Go to Dashboard
3. Click "Create New Run"
4. Enter issue URL and repository
5. Watch the AI-powered workflow in action!

## 🏗️ Architecture

### **Backend (FastAPI)**

- **Portia Integration**: Advanced AI workflow orchestration and issue analysis
- **OpenAI Integration**: Intelligent content generation and fix creation
- **GitHub API**: Real repository operations (branches, PRs, files)
- **Workflow Engine**: State machine with approval gates and risk assessment
- **REST API**: Clean endpoints for frontend integration

### **Frontend (Next.js 14)**

- **Modern UI**: Beautiful, responsive design with dark mode
- **Real-time Updates**: Live status monitoring and progress tracking
- **Dashboard**: Comprehensive overview of all runs
- **Interactive Workflow**: Approve/reject gates with detailed risk assessment

### **AI-Powered Features**

- **Portia Analysis**: Deep issue understanding with root cause analysis
- **Intelligent Fix Generation**: AI-powered code fixes and test cases
- **Risk Assessment**: Comprehensive safety and quality evaluation
- **Context-Aware Solutions**: Project-specific recommendations and best practices

## 📁 Project Structure

```
AI-Powered-Bug-to-PR-Autopilot-with-Portia-Integration/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── services/
│   │   ├── runs.py            # Run management and workflow
│   │   ├── github.py          # GitHub API integration
│   │   ├── ai_fix_generator.py # AI-powered fix generation
│   │   ├── intelligent_fix.py  # Intelligent fix logic
│   │   ├── portia_service.py   # Portia AI integration
│   │   └── repo_analyzer.py    # Repository analysis
│   └── agent/
│       ├── plan.py            # Workflow plan definition
│       └── portia_integration.py # Portia SDK integration
├── frontend/
│   ├── app/
│   │   ├── page.tsx           # Landing page
│   │   ├── dashboard/         # Main dashboard
│   │   ├── runs/[id]/         # Run details
│   │   └── components/        # UI components
│   └── tailwind.config.js     # Styling configuration
├── config/
│   └── config.yaml            # Repository allowlist and settings
├── install_and_run.py         # One-command setup and run
├── test_ai_powered.py         # AI integration test
├── PROJECT_DETAILS.md         # Comprehensive project documentation
└── README.md                  # This file
```

> 📖 **For detailed project information, architecture, and technical details, see [PROJECT_DETAILS.md](PROJECT_DETAILS.md)**

## 🔧 Configuration

### **Repository Allowlist**

Edit `config/config.yaml` to add repositories:

```yaml
allowlist:
  - "your-username/your-repo"
  - "organization/repository"
```

### **Environment Variables**

```bash
# Required
GITHUB_TOKEN=ghp_your_token_here
OPENAI_API_KEY=sk-your_key_here
PORTIA_API_KEY=your_portia_key_here

# Optional
PORTIA_API_ENDPOINT=https://api.portialabs.ai
```

## 🎯 Example Workflow

### **1. Issue Analysis with Portia**

Portia AI analyzes the GitHub issue:

```json
{
  "issue_classification": {
    "type": "bug",
    "severity": "high",
    "complexity": "moderate",
    "impact_scope": "module-wide"
  },
  "root_cause_analysis": {
    "primary_cause": "Race condition in data processing",
    "contributing_factors": ["Async operations", "Missing locks"],
    "system_implications": "Data corruption in high-load scenarios"
  }
}
```

### **2. Intelligent Fix Generation**

AI creates comprehensive solution:

```python
# Generated test case
def test_data_race_condition():
    """Test to reproduce the race condition issue"""
    # Test implementation
    pass

# Generated fix
def fix_data_race_condition():
    """Fix for the race condition using proper locking"""
    # Fix implementation
    pass
```

### **3. Professional PR Creation**

AI generates comprehensive PR:

- **Title**: "Fix race condition in data processing module"
- **Body**: Detailed description with risk assessment and impact analysis
- **Files**: All necessary files with proper content and tests

## 🚨 Troubleshooting

### **Common Issues**

#### **"Portia API key not found"**

```bash
export PORTIA_API_KEY=your_portia_key_here
# Or add to .env file
```

#### **"OpenAI API key not found"**

```bash
export OPENAI_API_KEY=sk-your_key_here
# Or add to .env file
```

#### **"GitHub token not found"**

```bash
export GITHUB_TOKEN=ghp_your_token_here
# Or add to .env file
```

#### **"Port already in use"**

```bash
# Kill existing processes
pkill -f "uvicorn"
pkill -f "next"
```

#### **"Python version error"**

```bash
# Install Python 3.9+
brew install python@3.12  # macOS
# or
sudo apt install python3.9  # Ubuntu
```

### **Getting Help**

1. Check the logs for error messages
2. Verify your API keys are correct
3. Test with `python test_ai_powered.py`
4. Check service status at `http://localhost:8000/health`

## 🎉 Features

### **Portia AI-Powered Intelligence**

- ✅ **Advanced Issue Analysis**: Deep understanding with root cause analysis
- ✅ **Intelligent Workflow Planning**: Optimal process design based on context
- ✅ **Risk Assessment**: Comprehensive safety and quality evaluation
- ✅ **Context-Aware Recommendations**: Project-specific solutions

### **OpenAI-Powered Content Generation**

- ✅ **Smart Fix Generation**: Creates specific solutions for each issue
- ✅ **Test Case Creation**: Generates comprehensive test scenarios
- ✅ **Professional Documentation**: Creates detailed PR descriptions
- ✅ **Code Quality**: Ensures adherence to best practices

### **GitHub Integration**

- ✅ **Real PR Creation**: Creates actual pull requests in your repository
- ✅ **Branch Management**: Automatically creates and manages branches
- ✅ **File Operations**: Creates, updates, and manages repository files
- ✅ **Issue Comments**: Adds professional comments to original issues

### **Workflow Management**

- ✅ **Human-in-the-Loop Approval**: Two-stage approval process
- ✅ **Real-time Monitoring**: Live status updates and progress tracking
- ✅ **Comprehensive Logging**: Detailed logs of all operations
- ✅ **Error Handling**: Graceful fallbacks and error recovery

### **Modern UI/UX**

- ✅ **Responsive Design**: Works on desktop, tablet, and mobile
- ✅ **Dark Mode**: Beautiful dark/light theme support
- ✅ **Real-time Updates**: Live status monitoring
- ✅ **Interactive Dashboard**: Comprehensive overview and management

## 🔒 Security & Privacy

### **API Key Security**

- Keys are stored in environment variables
- No hardcoded secrets in the codebase
- Secure HTTPS connections to all APIs

### **Data Privacy**

- Only issue content is sent to AI services for analysis
- No data is stored beyond the API call
- All operations are logged for transparency

### **Repository Security**

- Repository allowlist prevents unauthorized access
- GitHub token has minimal required permissions
- All operations are logged and auditable

## 🚀 Next Steps

Once the system is running:

1. **Test with Different Issues**: Try various types of issues to see AI capabilities
2. **Customize AI Prompts**: Modify prompts in `backend/services/ai_fix_generator.py`
3. **Add More Repositories**: Update `config/config.yaml` with your repositories
4. **Monitor Usage**: Keep track of API usage and costs
5. **Scale Up**: Use for multiple repositories and teams

## 📞 Support

### **Getting Help**

1. Check the troubleshooting section above
2. Review the logs for error messages
3. Test with the AI-powered test script
4. Check service health endpoints

### **Useful Commands**

```bash
# Test AI integration
python test_ai_powered.py

# Check service health
curl http://localhost:8000/health

# View logs
tail -f backend.log

# Restart services
python install_and_run.py
```

---

**The AI-Powered Bug-to-PR Autopilot with Portia Integration is ready to intelligently analyze issues and generate professional solutions!** 🚀
