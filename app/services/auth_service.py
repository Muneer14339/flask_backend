import secrets
import string
from datetime import datetime, timedelta
from app.models.user import User, PasswordResetToken
from app.utils.validators import Validators
from app.utils.jwt_utils import JWTUtils
from app.services.email_service import EmailService
from app.services.google_oauth_service import GoogleOAuthService
from app import db

class AuthService:
    """Authentication service - Business logic layer (WITHOUT Redis)"""
    
    def __init__(self):
        self.email_service = EmailService()
        self.google_oauth_service = GoogleOAuthService()
    
    def register_user(self, full_name, email, password):
        """Register new user with email and password"""
        try:
            # Validate inputs
            is_valid_name, name_error = Validators.validate_full_name(full_name)
            if not is_valid_name:
                return False, name_error, None, None
            
            is_valid_email, email_error = Validators.validate_email_format(email)
            if not is_valid_email:
                return False, email_error, None, None
            
            is_valid_password, password_error = Validators.validate_password(password)
            if not is_valid_password:
                return False, password_error, None, None
            
            # Check if user already exists
            existing_user = User.find_by_email(email)
            if existing_user:
                return False, "Email is already registered", None, None
            
            # Create new user
            user = User(
                full_name=Validators.sanitize_string(full_name),
                email=email,
                password=password,
                sign_in_method='email'
            )
            
            user.save()
            
            # Generate tokens
            tokens = JWTUtils.generate_tokens(user.id)
            
            # Update last sign in
            user.update_last_sign_in()
            user.save()
            
            return True, "User registered successfully", user, tokens
            
        except Exception as e:
            return False, f"Registration failed: {str(e)}", None, None
    
    def login_user(self, email, password):
        """Login user with email and password"""
        try:
            # Validate inputs
            is_valid_email, email_error = Validators.validate_email_format(email)
            if not is_valid_email:
                return False, email_error, None, None
            
            if not password:
                return False, "Password is required", None, None
            
            # Find user
            user = User.find_by_email(email)
            if not user:
                return False, "No user found with this email", None, None
            
            # Check if user is active
            if not user.is_active:
                return False, "User account has been disabled", None, None
            
            # Verify password
            if not user.check_password(password):
                return False, "Incorrect password", None, None
            
            # Generate tokens
            tokens = JWTUtils.generate_tokens(user.id)
            
            # Update last sign in
            user.update_last_sign_in()
            user.save()
            
            return True, "Login successful", user, tokens
            
        except Exception as e:
            return False, f"Login failed: {str(e)}", None, None
    
    def google_signin(self, google_token):
        """Sign in with Google OAuth token"""
        try:
            # Verify Google token and get user info
            is_valid, google_user_info = self.google_oauth_service.verify_token(google_token)
            if not is_valid:
                return False, "Invalid Google token", None, None
            
            # Check if user exists with Google ID
            user = User.find_by_google_id(google_user_info['sub'])
            
            if not user:
                # Check if user exists with same email
                user = User.find_by_email(google_user_info['email'])
                
                if user:
                    # Link Google account to existing user
                    user.google_id = google_user_info['sub']
                    user.sign_in_method = 'google'
                    user.email_verified = True
                    if not user.photo_url and google_user_info.get('picture'):
                        user.photo_url = google_user_info['picture']
                else:
                    # Create new user with Google account
                    user = User(
                        full_name=google_user_info.get('name', 'Unknown User'),
                        email=google_user_info['email'],
                        google_id=google_user_info['sub'],
                        photo_url=google_user_info.get('picture'),
                        sign_in_method='google'
                    )
                
                user.save()
            
            # Check if user is active
            if not user.is_active:
                return False, "User account has been disabled", None, None
            
            # Generate tokens
            tokens = JWTUtils.generate_tokens(user.id)
            
            # Update last sign in
            user.update_last_sign_in()
            user.save()
            
            return True, "Google sign-in successful", user, tokens
            
        except Exception as e:
            return False, f"Google sign-in failed: {str(e)}", None, None
    
    def forgot_password(self, email):
        """Send password reset email with OTP stored in database"""
        try:
            # Validate email
            is_valid_email, email_error = Validators.validate_email_format(email)
            if not is_valid_email:
                return False, email_error
            
            # Find user
            user = User.find_by_email(email)
            if not user:
                # Don't reveal that user doesn't exist for security
                return True, "If an account with this email exists, you will receive a password reset link"
            
            # Check if user is active
            if not user.is_active:
                return False, "User account has been disabled"
            
            # Generate OTP
            otp = self._generate_otp()
            
            # Create password reset token in database
            reset_token = PasswordResetToken(
                user_id=user.id,
                token=otp,  # Using OTP as token
                expires_at=datetime.utcnow() + timedelta(minutes=10)  # 10 minutes expiry
            )
            
            # Clean up old tokens for this user (optional)
            self._cleanup_expired_tokens(user.id)
            
            # Save new token
            reset_token.save()
            
            # Send OTP email
            success = self.email_service.send_password_reset_otp(email, user.full_name, otp)
            if not success:
                return False, "Failed to send reset email"
            
            return True, "Password reset code sent to your email"
            
        except Exception as e:
            return False, f"Failed to process password reset: {str(e)}"
    
    def verify_otp(self, email, otp):
        """Verify OTP for password reset using database storage"""
        try:
            # Validate inputs
            is_valid_email, email_error = Validators.validate_email_format(email)
            if not is_valid_email:
                return False, email_error, None
            
            is_valid_otp, otp_error = Validators.validate_otp(otp)
            if not is_valid_otp:
                return False, otp_error, None
            
            # Find user
            user = User.find_by_email(email)
            if not user:
                return False, "User not found", None
            
            # Find valid OTP token
            reset_token = PasswordResetToken.query.filter_by(
                user_id=user.id,
                token=otp,
                used=False
            ).filter(
                PasswordResetToken.expires_at > datetime.utcnow()
            ).first()
            
            if not reset_token:
                return False, "Invalid or expired OTP", None
            
            # Generate new password reset token (different from OTP)
            password_reset_token = self._generate_reset_token()
            
            # Create new token entry for password reset
            new_reset_token = PasswordResetToken(
                user_id=user.id,
                token=password_reset_token,
                expires_at=datetime.utcnow() + timedelta(hours=1)  # 1 hour for password reset
            )
            
            # Mark OTP as used
            reset_token.mark_as_used()
            
            # Save new reset token
            new_reset_token.save()
            
            return True, "OTP verified successfully", password_reset_token
            
        except Exception as e:
            return False, f"OTP verification failed: {str(e)}", None
    
    def reset_password(self, email, reset_token, new_password):
        """Reset user password with token from database"""
        try:
            # Validate inputs
            is_valid_email, email_error = Validators.validate_email_format(email)
            if not is_valid_email:
                return False, email_error
            
            is_valid_password, password_error = Validators.validate_password(new_password)
            if not is_valid_password:
                return False, password_error
            
            # Find user
            user = User.find_by_email(email)
            if not user:
                return False, "User not found"
            
            # Find valid reset token
            token_record = PasswordResetToken.query.filter_by(
                user_id=user.id,
                token=reset_token,
                used=False
            ).filter(
                PasswordResetToken.expires_at > datetime.utcnow()
            ).first()
            
            if not token_record:
                return False, "Invalid or expired reset token"
            
            # Update password
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            token_record.mark_as_used()
            
            # Clean up old tokens for this user
            self._cleanup_expired_tokens(user.id)
            
            return True, "Password reset successfully"
            
        except Exception as e:
            return False, f"Password reset failed: {str(e)}"
    
    def get_current_user(self, user_id):
        """Get current user by ID"""
        try:
            user = User.find_by_id(user_id)
            if not user:
                return False, "User not found", None
            
            if not user.is_active:
                return False, "User account has been disabled", None
            
            return True, "User retrieved successfully", user
            
        except Exception as e:
            return False, f"Failed to get user: {str(e)}", None
    
    def _generate_otp(self):
        """Generate 4-digit OTP"""
        return ''.join(secrets.choice(string.digits) for _ in range(4))
    
    def _generate_reset_token(self):
        """Generate secure reset token"""
        return secrets.token_urlsafe(32)
    
    def _cleanup_expired_tokens(self, user_id):
        """Clean up expired tokens for a user"""
        try:
            expired_tokens = PasswordResetToken.query.filter(
                PasswordResetToken.user_id == user_id,
                PasswordResetToken.expires_at < datetime.utcnow()
            ).all()
            
            for token in expired_tokens:
                db.session.delete(token)
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error cleaning up expired tokens: {e}")
    
    def cleanup_all_expired_tokens(self):
        """Clean up all expired tokens (can be called periodically)"""
        try:
            expired_tokens = PasswordResetToken.query.filter(
                PasswordResetToken.expires_at < datetime.utcnow()
            ).all()
            
            for token in expired_tokens:
                db.session.delete(token)
            
            db.session.commit()
            return len(expired_tokens)
        except Exception as e:
            db.session.rollback()
            print(f"Error cleaning up expired tokens: {e}")
            return 0