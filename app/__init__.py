# app/__init__.py - Updated with Loadout, Ballistic, and Training features
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
import os
from sqlalchemy import text

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

def create_app(config_name=None):
    """Application factory pattern with automatic table creation"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from .config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Import all models here to ensure they are registered with SQLAlchemy
    from .models.user import User, PasswordResetToken
    from .models.loadout import Rifle, Ammunition, Scope, Maintenance
    from .models.ballistic import DopeEntry, ZeroEntry, ChronographData, BallisticCalculation
    
    # Create database tables automatically if they don't exist
    with app.app_context():
        try:
            # Check if database connection works (SQLAlchemy 2.0+ compatible)
            with db.engine.connect() as connection:
                connection.execute(text('SELECT 1'))
            print("✅ Database connection successful")
            
            # Create all tables if they don't exist
            db.create_all()
            print("✅ Database tables created/verified successfully")
            
            # Check if tables exist by trying to query them
            try:
                user_count = db.session.execute(text('SELECT COUNT(*) FROM users')).scalar()
                print(f"✅ Users table ready (current count: {user_count})")
                
                # Check new tables
                rifle_count = db.session.execute(text('SELECT COUNT(*) FROM rifles')).scalar() if _table_exists('rifles') else 0
                ammo_count = db.session.execute(text('SELECT COUNT(*) FROM ammunition')).scalar() if _table_exists('ammunition') else 0
                scope_count = db.session.execute(text('SELECT COUNT(*) FROM scopes')).scalar() if _table_exists('scopes') else 0
                maintenance_count = db.session.execute(text('SELECT COUNT(*) FROM maintenance')).scalar() if _table_exists('maintenance') else 0
                
                print(f"✅ Loadout tables ready - Rifles: {rifle_count}, Ammunition: {ammo_count}, Scopes: {scope_count}, Maintenance: {maintenance_count}")
                
                dope_count = db.session.execute(text('SELECT COUNT(*) FROM dope_entries')).scalar() if _table_exists('dope_entries') else 0
                zero_count = db.session.execute(text('SELECT COUNT(*) FROM zero_entries')).scalar() if _table_exists('zero_entries') else 0
                chrono_count = db.session.execute(text('SELECT COUNT(*) FROM chronograph_data')).scalar() if _table_exists('chronograph_data') else 0
                calc_count = db.session.execute(text('SELECT COUNT(*) FROM ballistic_calculations')).scalar() if _table_exists('ballistic_calculations') else 0
                
                print(f"✅ Ballistic tables ready - DOPE: {dope_count}, Zero: {zero_count}, Chronograph: {chrono_count}, Calculations: {calc_count}")
                
                session_count = db.session.execute(text('SELECT COUNT(*) FROM training_sessions')).scalar() if _table_exists('training_sessions') else 0
                sensor_count = db.session.execute(text('SELECT COUNT(*) FROM sensor_data')).scalar() if _table_exists('sensor_data') else 0
                device_count = db.session.execute(text('SELECT COUNT(*) FROM device_connections')).scalar() if _table_exists('device_connections') else 0
                
                print(f"✅ Training tables ready - Sessions: {session_count}, Sensor Data: {sensor_count}, Devices: {device_count}")
                
            except Exception as e:
                print(f"⚠️  Table verification issue: {e}")
                # Try to create tables again
                db.create_all()
                print("✅ Tables recreated successfully")
                
        except Exception as e:
            print(f"❌ Database setup error: {e}")
            print("⚠️  Please check your database configuration in .env file")
    
    # Register blueprints
    from .views.auth import auth_bp
    from .views.loadout import loadout_bp
    from .views.ballistic import ballistic_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(loadout_bp, url_prefix='/api/loadout')
    app.register_blueprint(ballistic_bp, url_prefix='/api/ballistic')
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'message': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'message': 'Invalid token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'message': 'Authorization token is required'}, 401
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        try:
            # Test database connection (SQLAlchemy 2.0+ compatible)
            with db.engine.connect() as connection:
                connection.execute(text('SELECT 1'))
            return {
                'status': 'healthy', 
                'message': 'RifleAxis API is running',
                'database': 'connected',
                'features': ['auth', 'loadout', 'ballistic', 'training']
            }, 200
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': 'Database connection failed',
                'error': str(e)
            }, 500
    
    # Database info endpoint
    @app.route('/api/db-info')
    def database_info():
        try:
            from .models.user import User, PasswordResetToken
            from .models.loadout import Rifle, Ammunition, Scope, Maintenance
            from .models.ballistic import DopeEntry, ZeroEntry, ChronographData, BallisticCalculation
            
            user_count = db.session.execute(text('SELECT COUNT(*) FROM users')).scalar()
            token_count = db.session.execute(text('SELECT COUNT(*) FROM password_reset_tokens')).scalar()
            
            # Loadout counts
            rifle_count = db.session.execute(text('SELECT COUNT(*) FROM rifles')).scalar() if _table_exists('rifles') else 0
            ammo_count = db.session.execute(text('SELECT COUNT(*) FROM ammunition')).scalar() if _table_exists('ammunition') else 0
            scope_count = db.session.execute(text('SELECT COUNT(*) FROM scopes')).scalar() if _table_exists('scopes') else 0
            maintenance_count = db.session.execute(text('SELECT COUNT(*) FROM maintenance')).scalar() if _table_exists('maintenance') else 0
            
            # Ballistic counts
            dope_count = db.session.execute(text('SELECT COUNT(*) FROM dope_entries')).scalar() if _table_exists('dope_entries') else 0
            zero_count = db.session.execute(text('SELECT COUNT(*) FROM zero_entries')).scalar() if _table_exists('zero_entries') else 0
            chrono_count = db.session.execute(text('SELECT COUNT(*) FROM chronograph_data')).scalar() if _table_exists('chronograph_data') else 0
            calc_count = db.session.execute(text('SELECT COUNT(*) FROM ballistic_calculations')).scalar() if _table_exists('ballistic_calculations') else 0
            
    
            return {
                'status': 'success',
                'tables': {
                    'users': user_count,
                    'password_reset_tokens': token_count,
                    'rifles': rifle_count,
                    'ammunition': ammo_count,
                    'scopes': scope_count,
                    'maintenance': maintenance_count,
                    'dope_entries': dope_count,
                    'zero_entries': zero_count,
                    'chronograph_data': chrono_count,
                    'ballistic_calculations': calc_count,
                },
                'database': 'connected'
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Database query failed',
                'error': str(e)
            }, 500
    
    # Periodic cleanup endpoint (optional - can be called by cron job)
    @app.route('/api/cleanup-expired-tokens')
    def cleanup_expired_tokens():
        try:
            from .services.auth_service import AuthService
            auth_service = AuthService()
            cleaned_count = auth_service.cleanup_all_expired_tokens()
            return {
                'status': 'success',
                'message': f'Cleaned {cleaned_count} expired tokens'
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Cleanup failed',
                'error': str(e)
            }, 500
    
    return app

def _table_exists(table_name):
    """Check if a table exists in the database"""
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text(f"SELECT 1 FROM {table_name} LIMIT 1"))
            return True
    except:
        return False

def init_database():
    """Initialize database with tables and basic data"""
    try:
        from .models.user import User, PasswordResetToken
        from .models.loadout import Rifle, Ammunition, Scope, Maintenance
        from .models.ballistic import DopeEntry, ZeroEntry, ChronographData, BallisticCalculation
        
        # Create all tables
        db.create_all()
        
        # Optional: Create a test user for development
        if os.environ.get('FLASK_ENV') == 'development':
            test_user = User.find_by_email('admin@rifleaxis.com')
            if not test_user:
                test_user = User(
                    full_name='Admin User',
                    email='admin@rifleaxis.com',
                    password='Admin123!',
                    sign_in_method='email'
                )
                test_user.email_verified = True
                test_user.save()
                print("✅ Test admin user created: admin@rifleaxis.com / Admin123!")
                
                # Create sample data for development
                create_sample_data(test_user.id)
        
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def create_sample_data(user_id):
    """Create sample data for development/testing"""
    try:
        from .models.loadout import Rifle, Ammunition, Scope, Maintenance
        
        # Create sample rifle
        sample_rifle = Rifle.find_by_user_id(user_id)
        if not sample_rifle:
            rifle = Rifle(
                user_id=user_id,
                name='Sample AR-15',
                brand='BCM',
                manufacturer='Bravo Company MFG',
                generation_variant='RECCE-16',
                model='RECCE-16',
                caliber='5.56mm NATO',
                barrel={'length': '16"', 'twist': '1:7', 'profile': 'Lightweight'},
                action={'type': 'Semi-Automatic', 'trigger': 'BCM PNT'},
                stock={'manufacturer': 'BCM', 'model': 'Gunfighter', 'adjustableLOP': True, 'adjustableCheekRest': False},
                is_active=True,
                notes='Sample rifle for development'
            )
            rifle.save()
            print("✅ Sample rifle created")
            
            # Create sample ammunition
            ammunition = Ammunition(
                user_id=user_id,
                name='M855 Green Tip',
                manufacturer='Lake City',
                caliber='5.56mm NATO',
                bullet={'weight': '62gr', 'type': 'FMJ', 'bc': {'g1': 0.31}},
                count=1000,
                temp_stable=True,
                notes='Sample ammunition for development'
            )
            ammunition.save()
            print("✅ Sample ammunition created")
            
            # Create sample scope
            scope = Scope(
                user_id=user_id,
                manufacturer='Vortex',
                model='Viper PST Gen II 1-6x24',
                tube_size='30mm',
                focal_plane='FFP',
                reticle='VMR-2',
                tracking_units='MRAD',
                click_value='0.1 MRAD',
                total_travel={'elevation': '28 MRAD', 'windage': '14 MRAD'},
                zero_data=[{'distance': 100, 'units': 'yards', 'elevation': '0', 'windage': '0'}],
                notes='Sample scope for development'
            )
            scope.save()
            print("✅ Sample scope created")
            
            # Create sample maintenance task
            maintenance = Maintenance(
                user_id=user_id,
                rifle_id=rifle.id,
                title='Barrel Cleaning',
                type='Cleaning',
                interval={'value': 500, 'unit': 'rounds'},
                current_count=0,
                notes='Clean barrel every 500 rounds'
            )
            maintenance.save()
            print("✅ Sample maintenance task created")
            
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")