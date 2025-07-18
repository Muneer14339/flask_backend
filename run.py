import os
from app import create_app, db, init_database
from sqlalchemy import text

def setup_database():
    """Setup database automatically on startup"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Setting up database...")
            
            # Test database connection first (SQLAlchemy 2.0+ compatible)
            with db.engine.connect() as connection:
                connection.execute(text('SELECT 1'))
            print("✅ Database connection successful")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created/verified")
            
            # Initialize with basic data if needed
            init_database()
            
            return True
            
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            print("\n🔍 Troubleshooting tips:")
            print("1. Check if PostgreSQL is running")
            print("2. Verify DATABASE_URL in .env file")
            print("3. Ensure database 'rifleaxis_db' exists")
            print("4. Check database user permissions")
            print("\n💡 Quick PostgreSQL setup:")
            print("sudo -u postgres psql")
            print("CREATE DATABASE rifleaxis_db;")
            print("CREATE USER rifleaxis_user WITH PASSWORD 'mypassword123';")
            print("GRANT ALL PRIVILEGES ON DATABASE rifleaxis_db TO rifleaxis_user;")
            print("\\q")
            return False

def check_environment():
    """Check if required environment variables are set"""
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    env_file_path = os.path.join(os.getcwd(), '.env')
    print(f"🔍 Loading environment from: {env_file_path}")
    print(f"🔍 .env file exists: {os.path.exists(env_file_path)}")
    
    required_vars = ['DATABASE_URL']
    optional_vars = ['MAIL_USERNAME', 'GOOGLE_CLIENT_ID']
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            missing_required.append(var)
        else:
            print(f"✅ {var} is set")
    
    for var in optional_vars:
        value = os.environ.get(var)
        if not value:
            missing_optional.append(var)
        else:
            # Hide sensitive values
            if 'SECRET' in var or 'PASSWORD' in var:
                print(f"🔍 {var} from env: ***")
            else:
                print(f"🔍 {var} from env: {value}")
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        print("   Please check your .env file")
        return False
    
    if missing_optional:
        print(f"⚠️  Missing optional environment variables: {', '.join(missing_optional)}")
        print("   Some features may not work (email, Google OAuth)")
    
    return True

def main():
    """Main application entry point"""
    print("\n" + "="*60)
    print("🎯 RifleAxis Backend Starting...")
    print("="*60)
    
    # Check environment variables first
    if not check_environment():
        print("\n💡 Tip: Copy .env.template to .env and configure it")
        return
    
    # Setup database automatically
    if not setup_database():
        print("\n❌ Failed to setup database. Please check configuration.")
        return
    
    # Create app instance
    app = create_app()
    
    # Get configuration from environment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"""
📊 Configuration:
   Environment: {os.environ.get('FLASK_ENV', 'development')}
   Debug Mode: {debug}
   Host: {host}
   Port: {port}
   
🌐 API Endpoints:
   Base URL: http://localhost:{port}/api
   
🔐 Authentication:
   POST /api/auth/signup          - User registration
   POST /api/auth/login           - User login  
   POST /api/auth/google-signin   - Google OAuth login
   POST /api/auth/forgot-password - Request password reset
   POST /api/auth/verify-otp      - Verify OTP code
   POST /api/auth/reset-password  - Reset password
   GET  /api/auth/me              - Get current user (Protected)
   POST /api/auth/refresh         - Refresh JWT token
   POST /api/auth/logout          - Logout user
   
📊 System:
   GET  /api/health               - API health check
   GET  /api/db-info              - Database information
   GET  /api/cleanup-expired-tokens - Clean expired tokens
   
🎉 Backend is ready to serve!
""")
    
    try:
        # Run the application
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=debug  # Only use reloader in development
        )
    except KeyboardInterrupt:
        print("\n👋 Backend stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")

def create_test_data():
    """Create test data for development (optional)"""
    app = create_app()
    
    with app.app_context():
        from app.models.user import User
        
        # Create test users
        test_users = [
            {
                'full_name': 'John Doe',
                'email': 'john@rifleaxis.com',
                'password': 'TestPass123!'
            },
            {
                'full_name': 'Jane Smith', 
                'email': 'jane@rifleaxis.com',
                'password': 'TestPass123!'
            }
        ]
        
        for user_data in test_users:
            existing_user = User.find_by_email(user_data['email'])
            if not existing_user:
                user = User(
                    full_name=user_data['full_name'],
                    email=user_data['email'],
                    password=user_data['password'],
                    sign_in_method='email'
                )
                user.email_verified = True
                user.save()
                print(f"✅ Test user created: {user_data['email']}")

if __name__ == '__main__':
    # Check if this is a command line argument
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'create-test-data':
            print("🧪 Creating test data...")
            create_test_data()
            print("✅ Test data created")
        elif command == 'setup-db':
            print("🔧 Setting up database...")
            if setup_database():
                print("✅ Database setup complete")
            else:
                print("❌ Database setup failed")
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands:")
            print("  python run.py                - Start server")
            print("  python run.py setup-db       - Setup database only")
            print("  python run.py create-test-data - Create test users")
    else:
        # Normal startup
        main()