#!/usr/bin/env python3
"""
Debug script for Layout.tsx component
Helps identify and fix issues with the React component
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Check if node_modules exists
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        os.chdir(frontend_dir)
        try:
            subprocess.run(["npm", "install"], check=True)
            os.chdir("..")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    return True

def check_typescript_config():
    """Check TypeScript configuration"""
    print("🔍 Checking TypeScript configuration...")
    
    frontend_dir = Path("frontend")
    tsconfig = frontend_dir / "tsconfig.json"
    
    if not tsconfig.exists():
        print("❌ tsconfig.json not found")
        return False
    
    print("✅ TypeScript configuration found")
    return True

def check_layout_file():
    """Check if Layout.tsx exists and is valid"""
    print("🔍 Checking Layout.tsx...")
    
    layout_file = Path("frontend/src/components/Layout.tsx")
    
    if not layout_file.exists():
        print("❌ Layout.tsx not found")
        return False
    
    # Read and check the file
    try:
        with open(layout_file, 'r') as f:
            content = f.read()
        
        # Basic checks
        if 'export function Layout' in content:
            print("✅ Layout component found")
        else:
            print("❌ Layout component not found in file")
            return False
        
        if 'useState' in content and 'useLocation' in content:
            print("✅ React hooks imported")
        else:
            print("❌ Missing React hooks")
            return False
        
        if 'lucide-react' in content:
            print("✅ Lucide icons imported")
        else:
            print("❌ Missing Lucide icons")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading Layout.tsx: {e}")
        return False

def run_type_check():
    """Run TypeScript type checking"""
    print("🔍 Running TypeScript type check...")
    
    frontend_dir = Path("frontend")
    os.chdir(frontend_dir)
    
    try:
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ TypeScript type check passed")
            return True
        else:
            print("❌ TypeScript type check failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running type check: {e}")
        return False
    finally:
        os.chdir("..")

def suggest_fixes():
    """Suggest fixes for common issues"""
    print("\n🔧 Suggested fixes:")
    print("1. Make sure all dependencies are installed:")
    print("   cd frontend && npm install")
    print()
    print("2. If you get React type errors, try:")
    print("   npm install --save-dev @types/react @types/react-dom")
    print()
    print("3. If you get lucide-react errors, try:")
    print("   npm install lucide-react")
    print()
    print("4. If you get react-router-dom errors, try:")
    print("   npm install react-router-dom")
    print()
    print("5. To run the development server:")
    print("   cd frontend && npm run dev")
    print()
    print("6. To check for TypeScript errors:")
    print("   cd frontend && npx tsc --noEmit")

def main():
    """Main debug function"""
    print("🐛 Layout.tsx Debug Script")
    print("=" * 40)
    
    checks = [
        check_dependencies,
        check_typescript_config,
        check_layout_file,
        run_type_check
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
        print()
    
    if all_passed:
        print("✅ All checks passed! Layout component should work correctly.")
        print("\nTo test the component:")
        print("1. cd frontend")
        print("2. npm run dev")
        print("3. Open http://localhost:3000")
    else:
        print("❌ Some checks failed. See suggestions below.")
        suggest_fixes()

if __name__ == "__main__":
    main() 