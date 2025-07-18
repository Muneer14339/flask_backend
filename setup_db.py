#!/usr/bin/env python3
"""
Database Auto-Setup Script for RifleAxis Backend
This script automatically creates database and tables if they don't exist
"""

import os
import sys
import subprocess
from urllib.parse import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def parse_database_url(database_url):
    """Parse DATABASE_URL into components"""
    parsed = urlparse(database_url)
    return {
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 5432,
        'user': parsed.username,
        'password': parsed.password,
        'database': parsed.path[1:] if parsed.path else None  # Remove leading '/'
    }

def create_database_if_not_exists(db_config):
    """Create database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (without specific database)
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database='postgres'  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_config['database'],)
        )
        
        if cursor.fetchone():
            print(f"✅ Database '{db_config['database']}' already exists")
        else:
            # Create database
            cursor.execute(f'CREATE DATABASE "{db_config["database"]}"')
            print(f"✅ Database '{db_config['database']}' created successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Failed to create database: {e}")
        return False

def create_user_if_not_exists(db_config):
    """Create user if it doesn't exist"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            user='postgres',  # Use postgres superuser
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute(
            "SELECT 1 FROM pg_user WHERE usename = %s",
            (db_config['user'],)
        )
        
        if cursor.fetchone():
            print(f"✅ User '{db_config['user']}' already exists")
        else:
            # Create user
            cursor.execute(
                f"CREATE USER \"{db_config['user']}\" WITH ENCRYPTED PASSWORD %s",
                (db_config['password'],)
            )
            print(f"✅ User '{db_config['user']}' created successfully")
        
        # Grant privileges
        cursor.execute(
            f'GRANT ALL PRIVILEGES ON DATABASE "{db_config["database"]}" TO "{db_config["user"]}"'
        )
        print(f"✅ Privileges granted to '{db_config['user']}'")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Failed to create user: {e}")
        print("💡 Make sure you have PostgreSQL superuser access")
        return False

def test_connection(db_config):
    """Test database connection"""
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        conn.close()
        print("✅ Database connection test successful")
        return True
    except psycopg2.Error as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def setup_flask_app():
    """Setup Flask application and create tables"""
    try:
        # Set environment variable for Flask
        os.environ['FLASK_APP'] = 'run.py'
        
        # Try to import and setup the app
        try:
            from app import create_app, db
            from app.models.user import User, PasswordResetToken
            
            app = create_app()
            
            with app.app_context():
                # Create all tables
                db.create_all()
                print("✅ Database tables created successfully")
                
                # Test by creating a query
                user_count = User.query.count()
                token_count = PasswordResetToken.query.count()
                print(f"✅ Tables verified - Users: {user_count}, Tokens: {token_count}")
                
                return True
                
        except ImportError as e:
            print(f"❌ Failed to import Flask app: {e}")
            print("💡 Make sure you're in the correct directory and virtual environment is activated")
            return False
            
    except Exception as e:
        print(f"❌ Failed to setup Flask app: {e}")
        return False

def main():
    """Main setup function"""
    print("🎯 RifleAxis Database Auto-Setup")
    print("=" * 40)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        if os.path.exists('.env.template'):
            print("⚠️  .env file not found. Creating from template...")
            subprocess.run(['cp', '.env.template', '.env'])
            print("✅ .env file created from template")
            print("🔧 Please edit .env file with your database credentials")
            return
        else:
            print("❌ No .env or .env.template file found")
            print("💡 Please create .env file with DATABASE_URL")
            return
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get database URL
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        print("💡 Please set DATABASE_URL in .env file")
        return
    
    print(f"🔧 Database URL: {database_url}")
    
    # Parse database configuration
    db_config = parse_database_url(database_url)
    print(f"🔧 Connecting to: {db_config['host']}:{db_config['port']}")
    
    # Step 1: Create database if needed
    print("\n📋 Step 1: Creating database...")
    if not create_database_if_not_exists(db_config):
        # If automatic creation fails, try alternative method
        print("⚠️  Trying alternative database creation...")
        
        print(f"""
💡 Manual database creation:
Run these commands in PostgreSQL:

sudo -u postgres psql
CREATE DATABASE {db_config['database']};
CREATE USER {db_config['user']} WITH ENCRYPTED PASSWORD '{db_config['password']}';
GRANT ALL PRIVILEGES ON DATABASE {db_config['database']} TO {db_config['user']};
\\q
        """)
    
    # Step 2: Test connection
    print("\n📋 Step 2: Testing connection...")
    if not test_connection(db_config):
        print("❌ Cannot continue without database connection")
        return
    
    # Step 3: Create Flask tables
    print("\n📋 Step 3: Creating application tables...")
    if setup_flask_app():
        print("\n🎉 Database setup completed successfully!")
        print("\n🚀 You can now start the backend with:")
        print("   python run.py")
    else:
        print("\n❌ Database setup failed")

if __name__ == '__main__':
    main()