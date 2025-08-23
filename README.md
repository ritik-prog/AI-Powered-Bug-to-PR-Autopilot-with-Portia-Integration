# 🤖 AI-Powered Bug-to-PR Autopilot

[🎥 Watch the demo](https://drive.google.com/file/d/1jeiM07y4YXAetEf8nGGxjW43lG2sX3yR/view?usp=sharing)

An intelligent automation system that uses **OpenAI AI** to analyze GitHub issues and automatically create professional pull requests with contextual fixes.

## 🎯 What It Does

This system automatically:

- **Analyzes GitHub issues** using AI to understand requirements
- **Generates intelligent fixes** based on issue context
- **Creates professional PRs** with comprehensive descriptions
- **Handles various issue types** (documentation, bugs, features, enhancements)
- **Provides real-time workflow** with approval gates

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

## 🧪 Testing

### **AI-Powered Test**

```bash
python test_ai_powered.py
```

This comprehensive test:

- ✅ Validates API key configuration
- ✅ Tests AI-powered issue analysis
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

- **AI Integration**: OpenAI-powered issue analysis and fix generation
- **GitHub API**: Real repository operations (branches, PRs, files)
- **Workflow Engine**: State machine with approval gates
- **REST API**: Clean endpoints for frontend integration

### **Frontend (Next.js 14)**

- **Modern UI**: Beautiful, responsive design with dark mode
- **Real-time Updates**: Live status monitoring and progress tracking
- **Dashboard**: Comprehensive overview of all runs
- **Interactive Workflow**: Approve/reject gates with comments

### **AI-Powered Features**

- **Intelligent Analysis**: Understands issue context and requirements
- **Custom Solutions**: Generates specific fixes for each issue type
- **Professional Quality**: Creates comprehensive, well-formatted content
- **Context-Aware**: Tailors solutions to repository and issue specifics

## 📁 Project Structure

```
autopilot_app_complete/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── services/
│   │   ├── runs.py            # Run management and workflow
│   │   ├── github.py          # GitHub API integration
│   │   └── ai_fix_generator.py # AI-powered fix generation
│   └── agent/
│       └── plan.py            # Workflow plan definition
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
├── AI_SETUP.md               # AI setup guide
├── setup_ai.sh               # AI setup helper
├── PROJECT_DETAILS.md        # Comprehensive project documentation
└── README.md                 # This file
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

# Optional
PORTIA_API_KEY=your_portia_key  # For advanced AI features
```

## 🎯 Example Workflow

### **1. Issue Analysis**

AI analyzes the GitHub issue:

```json
{
  "issue_type": "documentation",
  "priority": "medium",
  "required_actions": ["Create CONTRIBUTING.md"],
  "files_to_create": ["CONTRIBUTING.md"],
  "solution_approach": "Create comprehensive contributing guidelines"
}
```

### **2. Intelligent Fix Generation**

AI creates professional content:

```markdown
# Contributing to Your Repository

Thank you for your interest in contributing! This document provides...

## Getting Started

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Code of Conduct

We are committed to providing a welcoming environment...
```

### **3. Professional PR Creation**

AI generates comprehensive PR:

- **Title**: "Add CONTRIBUTING.md with comprehensive guidelines"
- **Body**: Detailed description with technical details and impact assessment
- **Files**: All necessary files with proper content

## 🚨 Troubleshooting

### **Common Issues**

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

### **AI-Powered Intelligence**

- ✅ **Smart Issue Analysis**: Understands context and requirements
- ✅ **Custom Fix Generation**: Creates specific solutions for each issue
- ✅ **Professional Quality**: Generates comprehensive, well-formatted content
- ✅ **Context-Aware**: Tailors solutions to repository specifics

### **GitHub Integration**

- ✅ **Real PR Creation**: Creates actual pull requests in your repository
- ✅ **Branch Management**: Automatically creates and manages branches
- ✅ **File Operations**: Creates, updates, and manages repository files
- ✅ **Issue Comments**: Adds professional comments to original issues

### **Workflow Management**

- ✅ **Approval Gates**: Human oversight with approve/reject options
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

- Only issue content is sent to OpenAI for analysis
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
4. **Monitor Usage**: Keep track of OpenAI API usage and costs
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

**The AI-Powered Bug-to-PR Autopilot is ready to intelligently analyze issues and generate professional solutions!** 🚀
