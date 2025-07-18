from app.services.auth_service import AuthService
from app.utils.responses import ApiResponse
import logging

class AuthViewModel:
    """Auth ViewModel - Handles business logic for authentication views"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def handle_user_registration(self, request_data):
        """Handle user registration request"""
        try:
            # Extract data from request
            full_name = request_data.get('fullName', '').strip()
            email = request_data.get('email', '').strip()
            password = request_data.get('password', '')
            
            # Validate required fields
            if not full_name:
                return ApiResponse.validation_error("Full name is required")
            
            if not email:
                return ApiResponse.validation_error("Email is required")
            
            if not password:
                return ApiResponse.validation_error("Password is required")
            
            # Call service layer
            success, message, user, tokens = self.auth_service.register_user(
                full_name, email, password
            )
            
            if success:
                return ApiResponse.auth_success(user, tokens, "Registration successful")
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Registration error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Registration failed")
    
    def handle_user_login(self, request_data):
        """Handle user login request"""
        try:
            # Extract data from request
            email = request_data.get('email', '').strip()
            password = request_data.get('password', '')
            
            # Validate required fields
            if not email:
                return ApiResponse.validation_error("Email is required")
            
            if not password:
                return ApiResponse.validation_error("Password is required")
            
            # Call service layer
            success, message, user, tokens = self.auth_service.login_user(email, password)
            
            if success:
                return ApiResponse.auth_success(user, tokens, "Login successful")
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Login error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Login failed")
    
    def handle_google_signin(self, request_data):
        """Handle Google sign-in request"""
        try:
            # Extract Google token from request
            google_token = request_data.get('googleToken', '')
            
            # Validate required fields
            if not google_token:
                return ApiResponse.validation_error("Google token is required")
            
            # Call service layer
            success, message, user, tokens = self.auth_service.google_signin(google_token)
            
            if success:
                return ApiResponse.auth_success(user, tokens, "Google sign-in successful")
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Google sign-in error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Google sign-in failed")
    
    def handle_forgot_password(self, request_data):
        """Handle forgot password request"""
        try:
            # Extract email from request
            email = request_data.get('email', '').strip()
            
            # Validate required fields
            if not email:
                return ApiResponse.validation_error("Email is required")
            
            # Call service layer
            success, message = self.auth_service.forgot_password(email)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Forgot password error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to process password reset request")
    
    def handle_verify_otp(self, request_data):
        """Handle OTP verification request"""
        try:
            # Extract data from request
            email = request_data.get('email', '').strip()
            otp = request_data.get('otp', '').strip()
            
            # Validate required fields
            if not email:
                return ApiResponse.validation_error("Email is required")
            
            if not otp:
                return ApiResponse.validation_error("OTP is required")
            
            # Call service layer
            success, message, reset_token = self.auth_service.verify_otp(email, otp)
            
            if success:
                return ApiResponse.success(
                    data={'resetToken': reset_token},
                    message=message
                )
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"OTP verification error in ViewModel: {str(e)}")
            return ApiResponse.server_error("OTP verification failed")
    
    def handle_reset_password(self, request_data):
        """Handle password reset request"""
        try:
            # Extract data from request
            email = request_data.get('email', '').strip()
            reset_token = request_data.get('resetToken', '').strip()
            new_password = request_data.get('newPassword', '')
            
            # Validate required fields
            if not email:
                return ApiResponse.validation_error("Email is required")
            
            if not reset_token:
                return ApiResponse.validation_error("Reset token is required")
            
            if not new_password:
                return ApiResponse.validation_error("New password is required")
            
            # Call service layer
            success, message = self.auth_service.reset_password(email, reset_token, new_password)
            
            if success:
                return ApiResponse.success(message=message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Password reset error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Password reset failed")
    
    def handle_get_current_user(self, user_id):
        """Handle get current user request"""
        try:
            # Call service layer
            success, message, user = self.auth_service.get_current_user(user_id)
            
            if success:
                return ApiResponse.user_response(user, message)
            else:
                return ApiResponse.error(message)
                
        except Exception as e:
            logging.error(f"Get current user error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Failed to get user information")
    
    def handle_refresh_token(self, user_id):
        """Handle token refresh request"""
        try:
            from app.utils.jwt_utils import JWTUtils
            
            # Generate new access token
            new_tokens = JWTUtils.refresh_access_token(user_id)
            
            return ApiResponse.success(
                data={'tokens': new_tokens},
                message="Token refreshed successfully"
            )
            
        except Exception as e:
            logging.error(f"Token refresh error in ViewModel: {str(e)}")
            return ApiResponse.server_error("Token refresh failed")