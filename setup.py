#!/usr/bin/env python3
"""
Setup script for Pot Logic Poker Bot
Installs dependencies and initializes the project
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        print(f"✅ Node.js {result.stdout.strip()} detected")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js is required but not found")
        print("Please install Node.js from https://nodejs.org/")
        return False

def install_backend_dependencies():
    """Install Python backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("venv")
    if not venv_path.exists():
        print("🔄 Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv venv", "Creating virtual environment"):
            return False
    
    # Determine the correct pip path
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
        python_path = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    # Install requirements
    if not run_command(f"{pip_path} install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    return True

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("\n📦 Installing frontend dependencies...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Install npm dependencies
    if not run_command("npm install", "Installing npm dependencies"):
        return False
    
    # Change back to root directory
    os.chdir("..")
    return True

def create_env_file():
    """Create .env file from example"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        print("🔄 Creating .env file from template...")
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ .env file created")
        return True
    else:
        print("⚠️  No env.example file found, creating basic .env file...")
        with open(env_file, "w") as f:
            f.write("DATABASE_URL=sqlite:///./poker_bot.db\n")
            f.write("SECRET_KEY=your-secret-key-here-change-this-in-production\n")
            f.write("DEBUG=True\n")
        print("✅ Basic .env file created")
        return True

def initialize_database():
    """Initialize the database"""
    print("\n🗄️  Initializing database...")
    
    # Import and run database initialization
    try:
        sys.path.append(str(Path.cwd()))
        from app.database import init_db
        import asyncio
        
        # Run async initialization
        asyncio.run(init_db())
        print("✅ Database initialized")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🎰 Pot Logic - Advanced Poker Bot Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check system requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_backend_dependencies():
        print("❌ Backend setup failed")
        sys.exit(1)
    
    if not install_frontend_dependencies():
        print("❌ Frontend setup failed")
        sys.exit(1)
    
    # Create environment file
    if not create_env_file():
        print("❌ Environment setup failed")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        print("❌ Database setup failed")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Copy env.example to .env and configure your settings")
    print("2. Run 'python start.py' to start both servers")
    print("3. Open http://localhost:3000 in your browser")
    print("\nFor development:")
    print("- Backend: python -m uvicorn app.main:app --reload")
    print("- Frontend: cd frontend && npm run dev")

if __name__ == "__main__":
    main() 