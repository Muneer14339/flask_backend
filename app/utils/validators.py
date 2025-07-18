import re
from email_validator import validate_email, EmailNotValidError

class Validators:
    """Validation utility functions"""
    
    @staticmethod
    def validate_email_format(email):
        """Validate email format"""
        try:
            validate_email(email)
            return True, None
        except EmailNotValidError as e:
            return False, str(e)
    
    @staticmethod
    def validate_password(password):
        """
        Validate password strength
        Requirements:
        - At least 8 characters
        - At least one uppercase letter
        - At least one number
        - At least one special character
        """
        if not password:
            return False, "Password is required"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        
        return True, None
    
    @staticmethod
    def validate_full_name(full_name):
        """Validate full name"""
        if not full_name or not full_name.strip():
            return False, "Full name is required"
        
        if len(full_name.strip()) < 2:
            return False, "Full name must be at least 2 characters long"
        
        if len(full_name.strip()) > 255:
            return False, "Full name must be less than 255 characters"
        
        return True, None
    
    @staticmethod
    def validate_otp(otp):
        """Validate OTP format"""
        if not otp:
            return False, "OTP is required"
        
        if not otp.isdigit():
            return False, "OTP must contain only numbers"
        
        if len(otp) != 4:
            return False, "OTP must be 4 digits"
        
        return True, None
    
    @staticmethod
    def sanitize_string(text, max_length=255):
        """Sanitize string input"""
        if not text:
            return ""
        
        # Strip whitespace and limit length
        sanitized = text.strip()[:max_length]
        
        # Remove potentially harmful characters
        sanitized = re.sub(r'[<>"\']', '', sanitized)
        
        return sanitized