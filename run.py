# run.py - Updated with complete RifleAxis API
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
    print("\n" + "="*70)
    print("🎯 RifleAxis Backend - Complete API with Loadout, Ballistic & Training")
    print("="*70)
    
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
   
🌐 API Base URL: http://localhost:{port}/api

🔐 Authentication Endpoints:
   POST /api/auth/signup          - User registration
   POST /api/auth/login           - User login  
   POST /api/auth/google-signin   - Google OAuth login
   POST /api/auth/forgot-password - Request password reset
   POST /api/auth/verify-otp      - Verify OTP code
   POST /api/auth/reset-password  - Reset password
   GET  /api/auth/me              - Get current user (Protected)
   POST /api/auth/refresh         - Refresh JWT token
   POST /api/auth/logout          - Logout user

🔫 Loadout Management Endpoints:
   GET  /api/loadout/rifles              - Get all rifles
   POST /api/loadout/rifles              - Create rifle
   GET  /api/loadout/rifles/<id>         - Get specific rifle
   PUT  /api/loadout/rifles/<id>         - Update rifle
   DELETE /api/loadout/rifles/<id>       - Delete rifle
   POST /api/loadout/rifles/set-active   - Set active rifle
   PUT  /api/loadout/rifles/<id>/scope   - Update rifle scope
   PUT  /api/loadout/rifles/<id>/ammunition - Update rifle ammunition
   
   GET  /api/loadout/ammunition          - Get all ammunition
   POST /api/loadout/ammunition          - Create ammunition
   PUT  /api/loadout/ammunition/<id>     - Update ammunition
   DELETE /api/loadout/ammunition/<id>   - Delete ammunition
   
   GET  /api/loadout/scopes              - Get all scopes
   POST /api/loadout/scopes              - Create scope
   PUT  /api/loadout/scopes/<id>         - Update scope
   DELETE /api/loadout/scopes/<id>       - Delete scope
   
   GET  /api/loadout/maintenance         - Get maintenance tasks
   POST /api/loadout/maintenance         - Create maintenance task
   POST /api/loadout/maintenance/<id>/complete - Complete maintenance
   DELETE /api/loadout/maintenance/<id>  - Delete maintenance task
   
   GET  /api/loadout/summary             - Get complete loadout summary

🎯 Ballistic Data Endpoints:
   GET  /api/ballistic/dope              - Get DOPE entries
   POST /api/ballistic/dope              - Create DOPE entry
   DELETE /api/ballistic/dope/<id>       - Delete DOPE entry
   
   GET  /api/ballistic/zero              - Get zero entries
   POST /api/ballistic/zero              - Create zero entry
   DELETE /api/ballistic/zero/<id>       - Delete zero entry
   
   GET  /api/ballistic/chronograph       - Get chronograph data
   POST /api/ballistic/chronograph       - Create chronograph data
   DELETE /api/ballistic/chronograph/<id> - Delete chronograph data
   
   GET  /api/ballistic/calculations      - Get ballistic calculations
   POST /api/ballistic/calculations      - Calculate ballistics
   DELETE /api/ballistic/calculations/<id> - Delete calculation
   
   GET  /api/ballistic/summary           - Get ballistic summary
   GET  /api/ballistic/all-data          - Get all ballistic data

🏋️ Training Session Endpoints:
   GET  /api/training/sessions           - Get training sessions
   POST /api/training/sessions           - Create training session
   GET  /api/training/sessions/<id>      - Get specific session
   PUT  /api/training/sessions/<id>      - Update session
   DELETE /api/training/sessions/<id>    - Delete session
   POST /api/training/sessions/<id>/start - Start session
   POST /api/training/sessions/<id>/end  - End session
   
   POST /api/training/sensor-data        - Save sensor data
   GET  /api/training/sessions/<id>/sensor-data - Get sensor data
   GET  /api/training/sessions/<id>/sensor-data/latest - Get latest data
   
   GET  /api/training/devices            - Get devices
   POST /api/training/devices            - Register device
   POST /api/training/devices/connect    - Connect device
   POST /api/training/devices/disconnect - Disconnect device
   POST /api/training/devices/calibrate  - Calibrate device
   GET  /api/training/devices/status     - Get device status
   
   GET  /api/training/statistics         - Get training statistics
   GET  /api/training/sessions/<id>/analytics - Get session analytics
   GET  /api/training/dashboard          - Get training dashboard

📊 System Endpoints:
   GET  /api/health                      - API health check
   GET  /api/db-info                     - Database information
   GET  /api/cleanup-expired-tokens      - Clean expired tokens

🔧 Authentication:
   - All protected endpoints require Authorization header: "Bearer <token>"
   - Use /api/auth/login or /api/auth/signup to get tokens
   - Use /api/auth/refresh to refresh expired tokens

📱 Flutter Integration:
   - Replace Firebase calls with HTTP requests to these endpoints
   - Use same data structures as Firebase (JSON compatible)
   - JWT tokens replace Firebase Auth tokens
   - Real-time updates available via polling or webhooks

🎉 Backend is ready to serve Flutter app!
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
        from app.models.loadout import Rifle, Ammunition, Scope, Maintenance
        from app.models.ballistic import DopeEntry, ZeroEntry, ChronographData
        
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
                
                # Create sample data for the user
                create_user_sample_data(user.id)

def create_user_sample_data(user_id):
    """Create comprehensive sample data for a user"""
    from app.models.loadout import Rifle, Ammunition, Scope, Maintenance
    from app.models.ballistic import DopeEntry, ZeroEntry, ChronographData
    
    try:
        # Create sample rifle
        rifle = Rifle(
            user_id=user_id,
            name='Precision AR-15',
            brand='Daniel Defense',
            manufacturer='Daniel Defense',
            generation_variant='DDM4 V7',
            model='DDM4 V7',
            caliber='5.56mm NATO',
            barrel={'length': '16"', 'twist': '1:7', 'profile': 'S2W', 'material': 'Chrome Moly Vanadium'},
            action={'type': 'Semi-Automatic', 'trigger': 'Geissele SSA-E', 'triggerWeight': '3.5 lbs'},
            stock={'manufacturer': 'Daniel Defense', 'model': 'Sopmod', 'adjustableLOP': True, 'adjustableCheekRest': False},
            is_active=True,
            serial_number='DD12345678',
            notes='Primary precision rifle'
        )
        rifle.save()
        
        # Create sample ammunition
        ammunition = Ammunition(
            user_id=user_id,
            name='Black Hills 77gr TMK',
            manufacturer='Black Hills',
            caliber='5.56mm NATO',
            bullet={'weight': '77gr', 'type': 'TMK', 'manufacturer': 'Sierra', 'bc': {'g1': 0.42, 'g7': 0.22}},
            velocity=2750,
            count=500,
            temp_stable=True,
            cartridge_type='Factory',
            case_material='Brass',
            primer_type='Boxer',
            notes='Match grade ammunition'
        )
        ammunition.save()
        
        # Create sample scope
        scope = Scope(
            user_id=user_id,
            manufacturer='Nightforce',
            model='ATACR 4-16x42 F1',
            tube_size='30mm',
            focal_plane='FFP',
            reticle='MOAR',
            tracking_units='MOA',
            click_value='1/4 MOA',
            total_travel={'elevation': '100 MOA', 'windage': '60 MOA'},
            zero_data=[
                {'distance': 100, 'units': 'yards', 'elevation': '0', 'windage': '0'},
                {'distance': 200, 'units': 'yards', 'elevation': '2.5', 'windage': '0'}
            ],
            notes='Primary optic for precision shooting'
        )
        scope.save()
        
        # Update rifle with scope and ammunition
        rifle.scope_id = scope.id
        rifle.ammunition_id = ammunition.id
        rifle.save()
        
        # Create sample maintenance tasks
        maintenance_tasks = [
            {
                'title': 'Barrel Cleaning',
                'type': 'Cleaning',
                'interval': {'value': 500, 'unit': 'rounds'},
                'notes': 'Clean barrel every 500 rounds'
            },
            {
                'title': 'Bolt Lubrication',
                'type': 'Lubrication',
                'interval': {'value': 1000, 'unit': 'rounds'},
                'notes': 'Lubricate bolt and carrier group'
            },
            {
                'title': 'Scope Mount Torque Check',
                'type': 'Maintenance',
                'interval': {'value': 6, 'unit': 'months'},
                'torque_spec': '18 ft-lbs',
                'notes': 'Check scope ring and base torque'
            }
        ]
        
        for task_data in maintenance_tasks:
            maintenance = Maintenance(
                user_id=user_id,
                rifle_id=rifle.id,
                title=task_data['title'],
                type=task_data['type'],
                interval=task_data['interval'],
                torque_spec=task_data.get('torque_spec'),
                notes=task_data['notes']
            )
            maintenance.save()
        
        # Create sample ballistic data
        # DOPE entries
        dope_entries = [
            {'distance': 100, 'elevation': '0', 'windage': '0'},
            {'distance': 200, 'elevation': '2.5', 'windage': '0'},
            {'distance': 300, 'elevation': '6.75', 'windage': '0'},
            {'distance': 400, 'elevation': '12.5', 'windage': '0'},
            {'distance': 500, 'elevation': '20', 'windage': '0'}
        ]
        
        for dope_data in dope_entries:
            dope = DopeEntry(
                user_id=user_id,
                rifle_id=rifle.id,
                ammunition_id=ammunition.id,
                distance=dope_data['distance'],
                elevation=dope_data['elevation'],
                windage=dope_data['windage'],
                notes=f"DOPE for {dope_data['distance']} yards"
            )
            dope.save()
        
        # Zero entries
        zero = ZeroEntry(
            user_id=user_id,
            rifle_id=rifle.id,
            distance=100,
            poi_offset='0.5" high, 0.25" right',
            confirmed=True,
            notes='100 yard zero confirmed'
        )
        zero.save()
        
        # Chronograph data
        chrono = ChronographData(
            user_id=user_id,
            rifle_id=rifle.id,
            ammunition_id=ammunition.id,
            velocities=[2748, 2752, 2749, 2751, 2750, 2753, 2747, 2754, 2748, 2752],
            average=2750.4,
            extreme_spread=7,
            standard_deviation=2.3,
            notes='10-shot string from 20" barrel'
        )
        chrono.save()
        
       
        print(f"✅ Sample data created for user {user_id}")
        
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")

if __name__ == '__main__':
    # Check if this is a command line argument
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'create-test-data':
            print("🧪 Creating comprehensive test data...")
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
            print("  python run.py create-test-data - Create comprehensive test data")
    else:
        # Normal startup
        main()