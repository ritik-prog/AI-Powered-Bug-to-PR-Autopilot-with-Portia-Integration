"""
AI-Powered Bug-to-PR Autopilot - Installation and Run Helper

This script automates the setup and launch of the AI-powered Bug-to-PR Autopilot.
It performs the following steps:

1. Creates a local Python virtual environment (venv) if it doesn't exist
2. Installs Python dependencies including OpenAI SDK
3. Installs Node.js dependencies for the Next.js frontend
4. Sets up environment variables for GitHub and OpenAI integration
5. Starts the backend and frontend concurrently

Usage:
    python install_and_run.py

The backend will listen on port 8000 and the frontend on port 3000.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Union


def run_command(cmd: str, cwd: Union[Path, str, None] = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and handle errors gracefully."""
    print(f"\n💻 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    
    if result.stdout:
        print(f"📤 Output: {result.stdout}")
    if result.stderr:
        print(f"⚠️  Errors: {result.stderr}")
    
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {cmd}")
    
    return result


def check_python_version() -> None:
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        raise RuntimeError(f"Python 3.9+ required, found {version.major}.{version.minor}")


def ensure_virtualenv(venv_dir: Path) -> tuple[Path, Path]:
    """Create a Python virtual environment if it doesn't exist."""
    if not venv_dir.exists():
        print(f"🔧 Creating virtual environment at {venv_dir}")
        try:
            run_command(f"python3.12 -m venv {venv_dir}")
        except RuntimeError:
            # Fallback to python3 if python3.12 is not available
            run_command(f"python3 -m venv {venv_dir}")
    
    python_exec = venv_dir / "bin" / "python"
    pip_exec = venv_dir / "bin" / "pip"
    
    if not python_exec.exists():
        raise FileNotFoundError(f"Python executable not found at {python_exec}")
    
    return python_exec, pip_exec


def install_python_deps(pip_exec: Path) -> None:
    """Install backend Python dependencies including AI packages."""
    print("📦 Installing Python dependencies...")
    
    # Upgrade pip
    run_command(f"{pip_exec} install --upgrade pip", check=False)
    
    # Install core dependencies
    core_deps = [
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "requests",
        "httpx",
        "pytest"
    ]
    
    # Install AI dependencies
    ai_deps = [
        "openai==0.28",  # Use compatible version
        "portia-sdk-python"
    ]
    
    # Install all dependencies
    all_deps = core_deps + ai_deps
    run_command(f"{pip_exec} install {' '.join(all_deps)}")


def install_node_deps(frontend_dir: Path) -> None:
    """Install frontend Node.js dependencies."""
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        raise FileNotFoundError(f"Expected package.json in {frontend_dir}")
    
    node_modules = frontend_dir / "node_modules"
    if node_modules.exists():
        print("📦 node_modules already present; skipping npm install")
        return
    
    print("📦 Installing Node.js dependencies...")
    run_command("npm install", cwd=frontend_dir)


def setup_environment() -> None:
    """Set up environment variables for AI and GitHub integration."""
    print("🔧 Setting up environment variables...")
    
    # Check for existing environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not github_token:
        print("⚠️  GITHUB_TOKEN not found in environment")
        print("   Set it with: export GITHUB_TOKEN=your_github_token")
        print("   Or add it to a .env file")
    
    if not openai_key:
        print("⚠️  OPENAI_API_KEY not found in environment")
        print("   Set it with: export OPENAI_API_KEY=your_openai_key")
        print("   Or add it to a .env file")
        print("   Get one at: https://platform.openai.com/api-keys")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file template...")
        with open(env_file, "w") as f:
            f.write("# AI-Powered Bug-to-PR Autopilot Environment Variables\n")
            f.write("# Add your API keys here:\n")
            f.write("GITHUB_TOKEN=your_github_token_here\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
        print("✅ Created .env file template")
        print("   Please edit .env and add your actual API keys")


def check_services() -> None:
    """Check if required services are available."""
    print("🔍 Checking service availability...")
    
    # Check if ports are available
    try:
        import socket
        for port in [8000, 3000]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            if result == 0:
                print(f"⚠️  Port {port} is already in use")
    except ImportError:
        pass


def start_services(python_exec: Path, repo_root: Path, frontend_dir: Path) -> None:
    """Start the backend and frontend services."""
    print("\n🚀 Starting AI-Powered Bug-to-PR Autopilot...")
    print("   Backend: http://localhost:8000")
    print("   Frontend: http://localhost:3000")
    print("   Use Ctrl+C to stop both processes")
    
    # Set environment variables for the backend
    env = os.environ.copy()
    env['PYTHONPATH'] = str(repo_root)
    
    # Start backend
    backend_cmd = f"{python_exec} -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"
    backend_proc = subprocess.Popen(
        backend_cmd, 
        shell=True, 
        cwd=repo_root,
        env=env
    )
    
    # Wait a moment for backend to start
    import time
    time.sleep(3)
    
    # Start frontend
    frontend_cmd = "./node_modules/.bin/next dev"
    frontend_proc = subprocess.Popen(
        frontend_cmd, 
        shell=True, 
        cwd=frontend_dir
    )
    
    try:
        # Wait for either process to finish
        while True:
            if backend_proc.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
            if frontend_proc.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        backend_proc.terminate()
        frontend_proc.terminate()
        
        # Wait for processes to terminate
        try:
            backend_proc.wait(timeout=5)
            frontend_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("⚠️  Force killing processes...")
            backend_proc.kill()
            frontend_proc.kill()
        
        print("✅ Services stopped")


def main() -> None:
    """Main installation and run function."""
    try:
        print("🤖 AI-Powered Bug-to-PR Autopilot Setup")
        print("=" * 50)
        
        # Check Python version
        check_python_version()
        
        # Get paths
        repo_root = Path(__file__).resolve().parent
        venv_dir = repo_root / "venv"
        frontend_dir = repo_root / "frontend"
        
        # Setup environment
        setup_environment()
        
        # Check services
        check_services()
        
        # Create virtual environment
        python_exec, pip_exec = ensure_virtualenv(venv_dir)
        
        # Install dependencies
        install_python_deps(pip_exec)
        install_node_deps(frontend_dir)
        
        # Start services
        start_services(python_exec, repo_root, frontend_dir)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure you have Python 3.9+ installed")
        print("   2. Check that ports 8000 and 3000 are available")
        print("   3. Verify your API keys are set correctly")
        print("   4. Try running: python test_ai_powered.py")
        sys.exit(1)


if __name__ == "__main__":
    main()