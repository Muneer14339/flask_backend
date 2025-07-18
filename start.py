#!/usr/bin/env python3
"""
Simple Start Script for RifleAxis Backend
- Automatically creates tables if they don't exist
- Checks all requirements
- Starts the backend server

Usage: python start.py
"""

import os
import sys
import subprocess

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_virtual_env():
    """Check if virtual environment is activated"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
        return True
    else:
        print("⚠️  Virtual environment not detected")
        print("💡 Run: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'psycopg2', 'sqlalchemy']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages installed")
        return True

def check_env_file():
    """Check .env configuration"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.template'):
            print("⚠️  .env file not found. Creating from template...")
            try:
                with open('.env.template', 'r') as template:
                    content = template.read()
                with open('.env', 'w') as env_file:
                    env_file.write(content)
                print("✅ .env file created from template")
                print("🔧 Please edit .env file and run again")
                return False
            except Exception as e:
                print(f"❌ Failed to create .env: {e}")
                return False
        else:
            print("❌ No .env file found")
            print("💡 Create .env file with DATABASE_URL")
            return False
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not set in .env")
        return False
    
    if 'username:password@localhost' in database_url:
        print("⚠️  .env file contains template values")
        print("🔧 Please update DATABASE_URL in .env file")
        return False
    
    print("✅ .env file configured")
    return True

def check_postgresql():
    """Check PostgreSQL connection"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        import psycopg2
        from urllib.parse import urlparse
        
        database_url = os.environ.get('DATABASE_URL')
        parsed = urlparse(database_url)
        
        conn = psycopg2.connect(
            host=parsed.hostname or 'localhost',
            port=parsed.port or 5432,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path[1:] if parsed.path else None
        )
        conn.close()
        print("✅ PostgreSQL connection successful")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("💡 Check if PostgreSQL is running and credentials are correct")
        return False

def create_tables():
    """Create database tables if they don't exist"""
    try:
        from app import create_app, db
        from app.models.user import User, PasswordResetToken
        
        app = create_app()
        with app.app_context():
            # Create all tables
            db.create_all()
            
            # Test tables
            User.query.count()
            PasswordResetToken.query.count()
            
        print("✅ Database tables ready")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def start_backend():
    """Start the backend server"""
    try:
        print("\n🚀 Starting RifleAxis Backend...")
        print("Press Ctrl+C to stop\n")
        
        # Import and run
        from run import main
        main()
        
    except KeyboardInterrupt:
        print("\n👋 Backend stopped")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")

def main():
    """Main function with all checks"""
    print("🎯 RifleAxis Backend Startup Check")
    print("=" * 40)
    
    checks = [
        ("Python version", check_python),
        ("Virtual environment", check_virtual_env),
        ("Dependencies", check_dependencies),
        ("Environment config", check_env_file),
        ("PostgreSQL connection", check_postgresql),
        ("Database tables", create_tables)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n📋 Checking {check_name}...")
        if not check_func():
            all_passed = False
            break
    
    if all_passed:
        print("\n🎉 All checks passed!")
        start_backend()
    else:
        print(f"\n❌ Setup incomplete. Please fix the issues above.")
        print("\n💡 Quick setup commands:")
        print("   1. python3 -m venv venv")
        print("   2. source venv/bin/activate  # Linux/Mac")
        print("   3. pip install -r requirements.txt")
        print("   4. Edit .env file with your database settings")
        print("   5. python start.py")

if __name__ == '__main__':
    main()