"""
Phase 1: Environment Setup and Configuration Verification
This script verifies that all environment variables are properly configured
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_environment():
    """Check and verify all environment setup"""
    
    print("=" * 60)
    print("PHASE 1: ENVIRONMENT SETUP VERIFICATION")
    print("=" * 60)
    
    # Load environment variables
    env_file = Path(__file__).parent / '.env'
    
    if not env_file.exists():
        print("❌ .env file not found!")
        return False
    
    load_dotenv(env_file)
    
    print("\n📋 Environment Configuration:")
    print("-" * 60)
    
    # Check required variables
    required_vars = {
        'GOOGLE_API_KEY': 'Google Gemini API Key',
    }
    
    optional_vars = {
        'DATABASE_URL': 'PostgreSQL Database URL',
        'REDIS_URL': 'Redis Cache URL',
        'AWS_ACCESS_KEY': 'AWS S3 Access Key',
        'REACT_APP_API_URL': 'Frontend API URL',
    }
    
    all_configured = True
    
    # Check required variables
    print("\n🔴 REQUIRED:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != 'paste_your_gemini_api_key_here':
            print(f"  ✅ {var}: Configured")
        else:
            print(f"  ❌ {var}: MISSING - {description}")
            all_configured = False
    
    # Check optional variables
    print("\n🟡 OPTIONAL:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: Configured")
        else:
            print(f"  ⚪ {var}: Not configured (optional)")
    
    print("\n" + "=" * 60)
    
    if all_configured:
        print("✅ ENVIRONMENT SETUP COMPLETE!")
        print("=" * 60)
        return True
    else:
        print("⚠️  Please configure all required variables in .env file")
        print("=" * 60)
        return False

def check_python_packages():
    """Check if essential packages are installed"""
    
    print("\n📦 Python Packages Check:")
    print("-" * 60)
    
    essential_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'dotenv',
    ]
    
    available_packages = []
    missing_packages = []
    
    for package in essential_packages:
        try:
            __import__(package.replace('-', '_'))
            available_packages.append(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print("\n⚠️  Missing packages. Run:")
        print(f"  python -m pip install -r requirements.txt")
        return False
    
    return True

if __name__ == "__main__":
    print("\n🚀 Starting Phase 1 Setup...\n")
    
    env_ok = check_environment()
    pkg_ok = check_python_packages()
    
    print("\n" + "=" * 60)
    if env_ok and pkg_ok:
        print("Phase 1 Complete!")
        print("\nNext steps:")
        print("  1. Run: python -m pip install -r requirements.txt")
        print("  2. Run: python -m uvicorn api.main:app --reload")
        print("  3. Visit: http://localhost:8000/docs")
        sys.exit(0)
    else:
        print("Phase 1 Setup Incomplete")
        sys.exit(1)
