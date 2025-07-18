from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    """User Model - Represents users in the system"""
    
    __tablename__ = 'users'
    
    # Primary fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Nullable for Google OAuth users
    
    # Authentication fields
    google_id = Column(String(255), unique=True, nullable=True, index=True)
    email_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Profile fields
    photo_url = Column(Text, nullable=True)
    sign_in_method = Column(String(50), nullable=False, default='email')  # 'email' or 'google'
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_sign_in = Column(DateTime, nullable=True)
    
    def __init__(self, full_name, email, password=None, google_id=None, photo_url=None, sign_in_method='email'):
        self.full_name = full_name
        self.email = email.lower().strip()
        self.google_id = google_id
        self.photo_url = photo_url
        self.sign_in_method = sign_in_method
        
        if password:
            self.set_password(password)
        
        # Auto-verify email for Google users
        if sign_in_method == 'google':
            self.email_verified = True
    
    def set_password(self, password):
        """Hash and set password"""
        if password:
            self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def update_last_sign_in(self):
        """Update last sign in timestamp"""
        self.last_sign_in = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert user to dictionary for JSON response"""
        return {
            'id': self.id,
            'fullName': self.full_name,
            'email': self.email,
            'emailVerified': self.email_verified,
            'photoURL': self.photo_url,
            'signInMethod': self.sign_in_method,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'lastSignIn': self.last_sign_in.isoformat() if self.last_sign_in else None
        }
    
    def to_flutter_dict(self):
        """Convert user to dictionary matching Flutter UserModel"""
        return {
            'id': self.id,
            'fullName': self.full_name,
            'email': self.email
        }
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        return User.query.filter_by(email=email.lower().strip()).first()
    
    @staticmethod
    def find_by_google_id(google_id):
        """Find user by Google ID"""
        return User.query.filter_by(google_id=google_id).first()
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        return User.query.filter_by(id=user_id).first()
    
    def save(self):
        """Save user to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete user from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def __repr__(self):
        return f'<User {self.email}>'

# Password Reset Token Model
class PasswordResetToken(db.Model):
    """Password Reset Token Model"""
    
    __tablename__ = 'password_reset_tokens'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(36), db.ForeignKey('users.id'), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('reset_tokens', lazy=True))
    
    def __init__(self, user_id, token, expires_at):
        self.user_id = user_id
        self.token = token
        self.expires_at = expires_at
    
    def is_valid(self):
        """Check if token is valid (not used and not expired)"""
        return not self.used and self.expires_at > datetime.utcnow()
    
    def mark_as_used(self):
        """Mark token as used"""
        self.used = True
        db.session.commit()
    
    @staticmethod
    def find_valid_token(token):
        """Find valid token"""
        reset_token = PasswordResetToken.query.filter_by(token=token).first()
        if reset_token and reset_token.is_valid():
            return reset_token
        return None
    
    def save(self):
        """Save token to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e