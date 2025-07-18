import requests
import jwt
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from flask import current_app
import logging

class GoogleOAuthService:
    """Google OAuth service for handling Google Sign-In with debugging"""
    
    def __init__(self):
        self.client_id = None
        self.client_secret = None
    
    def _get_google_config(self):
        """Get Google OAuth configuration"""
        if not self.client_id:
            self.client_id = current_app.config.get('GOOGLE_CLIENT_ID')
            self.client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET')
        
        print(f"🔵 Google Client ID: {self.client_id}")
        print(f"🔵 Google Client Secret: {'***' if self.client_secret else 'Not set'}")
        
        if not self.client_id or not self.client_secret:
            print("❌ Google OAuth configuration not found in environment variables")
            return False
        return True
    
    def verify_token(self, token):
        """
        Verify Google ID token and return user information with debugging
        
        Args:
            token (str): Google ID token from client
            
        Returns:
            tuple: (is_valid: bool, user_info: dict or None)
        """
        try:
            print(f"🔵 Verifying Google token: {token[:50]}...")
            
            if not self._get_google_config():
                return False, None
            
            # Method 1: Try with google.oauth2.id_token (recommended)
            try:
                print("🔵 Attempting verification with google.oauth2.id_token...")
                idinfo = id_token.verify_oauth2_token(
                    token, 
                    google_requests.Request(), 
                    self.client_id
                )
                print("✅ Token verified successfully with google.oauth2.id_token")
                
            except Exception as e:
                print(f"❌ Method 1 failed: {str(e)}")
                
                # Method 2: Try manual verification with PyJWT (fallback)
                print("🔵 Attempting manual verification...")
                return self._verify_token_manually(token)
            
            # Check if token is from correct issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                print(f"❌ Wrong issuer: {idinfo.get('iss')}")
                return False, None
            
            # Check audience (client ID)
            if idinfo.get('aud') != self.client_id:
                print(f"❌ Wrong audience. Expected: {self.client_id}, Got: {idinfo.get('aud')}")
                return False, None
            
            # Token is valid, return user info
            user_info = {
                'sub': idinfo['sub'],  # Google user ID
                'email': idinfo['email'],
                'name': idinfo.get('name', ''),
                'given_name': idinfo.get('given_name', ''),
                'family_name': idinfo.get('family_name', ''),
                'picture': idinfo.get('picture', ''),
                'email_verified': idinfo.get('email_verified', False)
            }
            
            print(f"✅ User info extracted: {user_info['email']}")
            return True, user_info
            
        except ValueError as e:
            print(f"❌ ValueError during token verification: {str(e)}")
            return False, None
        except Exception as e:
            print(f"❌ Unexpected error during Google token verification: {str(e)}")
            return False, None
    
    def _verify_token_manually(self, token):
        """Manual token verification as fallback"""
        try:
            print("🔵 Attempting manual token verification...")
            
            # Decode without verification first to see the structure
            unverified = jwt.decode(token, options={"verify_signature": False})
            print(f"🔵 Token payload (unverified): {unverified}")
            
            # Get Google's public keys
            keys_response = requests.get('https://www.googleapis.com/oauth2/v3/certs')
            keys = keys_response.json()
            
            # Verify token manually
            header = jwt.get_unverified_header(token)
            key_id = header.get('kid')
            
            if key_id not in keys:
                print(f"❌ Key ID {key_id} not found in Google keys")
                return False, None
            
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(keys[key_id])
            
            # Verify the token
            payload = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience=self.client_id,
                issuer=['accounts.google.com', 'https://accounts.google.com']
            )
            
            print("✅ Token verified manually")
            
            user_info = {
                'sub': payload['sub'],
                'email': payload['email'],
                'name': payload.get('name', ''),
                'given_name': payload.get('given_name', ''),
                'family_name': payload.get('family_name', ''),
                'picture': payload.get('picture', ''),
                'email_verified': payload.get('email_verified', False)
            }
            
            return True, user_info
            
        except Exception as e:
            print(f"❌ Manual verification failed: {str(e)}")
            return False, None
    
    def exchange_code_for_token(self, authorization_code, redirect_uri):
        """
        Exchange authorization code for access token
        
        Args:
            authorization_code (str): Authorization code from Google
            redirect_uri (str): Redirect URI used in authorization request
            
        Returns:
            tuple: (success: bool, token_data: dict or error_message: str)
        """
        try:
            if not self._get_google_config():
                return False, "Google OAuth not configured"
            
            token_url = "https://oauth2.googleapis.com/token"
            
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': authorization_code,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri
            }
            
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            
            if 'id_token' in token_data:
                # Verify the ID token
                is_valid, user_info = self.verify_token(token_data['id_token'])
                if is_valid:
                    return True, {
                        'access_token': token_data.get('access_token'),
                        'id_token': token_data.get('id_token'),
                        'refresh_token': token_data.get('refresh_token'),
                        'user_info': user_info
                    }
                else:
                    return False, "Invalid ID token"
            else:
                return False, "No ID token in response"
                
        except requests.RequestException as e:
            print(f"❌ Error exchanging authorization code: {str(e)}")
            return False, f"Token exchange failed: {str(e)}"
        except Exception as e:
            print(f"❌ Unexpected error during token exchange: {str(e)}")
            return False, f"Unexpected error: {str(e)}"
    
    def get_user_info(self, access_token):
        """
        Get user information using access token
        
        Args:
            access_token (str): Google access token
            
        Returns:
            tuple: (success: bool, user_info: dict or error_message: str)
        """
        try:
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {'Authorization': f'Bearer {access_token}'}
            
            response = requests.get(user_info_url, headers=headers)
            response.raise_for_status()
            
            user_info = response.json()
            return True, user_info
            
        except requests.RequestException as e:
            print(f"❌ Error getting user info: {str(e)}")
            return False, f"Failed to get user info: {str(e)}"
        except Exception as e:
            print(f"❌ Unexpected error getting user info: {str(e)}")
            return False, f"Unexpected error: {str(e)}"
    
    def revoke_token(self, token):
        """
        Revoke Google access token
        
        Args:
            token (str): Token to revoke
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            revoke_url = f"https://oauth2.googleapis.com/revoke?token={token}"
            response = requests.post(revoke_url)
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Error revoking token: {str(e)}")
            return False