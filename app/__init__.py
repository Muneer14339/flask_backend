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
    
    # Import models here to ensure they are registered with SQLAlchemy
    from .models.user import User, PasswordResetToken
    
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
            except Exception as e:
                print(f"⚠️  Users table issue: {e}")
                # Try to create tables again
                db.create_all()
                print("✅ Tables recreated successfully")
                
        except Exception as e:
            print(f"❌ Database setup error: {e}")
            print("⚠️  Please check your database configuration in .env file")
    
    # Register blueprints
    from .views.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
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
                'database': 'connected'
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
            
            user_count = db.session.execute(text('SELECT COUNT(*) FROM users')).scalar()
            token_count = db.session.execute(text('SELECT COUNT(*) FROM password_reset_tokens')).scalar()
            
            return {
                'status': 'success',
                'tables': {
                    'users': user_count,
                    'password_reset_tokens': token_count
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

def init_database():
    """Initialize database with tables and basic data"""
    try:
        from .models.user import User, PasswordResetToken
        
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
        
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False