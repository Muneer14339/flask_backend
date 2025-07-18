from flask import current_app
from flask_mail import Message
from app import mail
import logging

class EmailService:
    """Email service for sending notifications"""
    
    def send_password_reset_otp(self, email, user_name, otp):
        """Send password reset OTP email"""
        try:
            subject = "RifleAxis - Password Reset Code"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Password Reset - RifleAxis</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f5f5f5;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: white;
                        border-radius: 12px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 30px 20px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                        font-weight: 600;
                    }}
                    .content {{
                        padding: 40px 30px;
                    }}
                    .greeting {{
                        font-size: 18px;
                        margin-bottom: 20px;
                        color: #333;
                    }}
                    .otp-container {{
                        background-color: #f8f9ff;
                        border: 2px solid #667eea;
                        border-radius: 8px;
                        padding: 20px;
                        text-align: center;
                        margin: 30px 0;
                    }}
                    .otp-code {{
                        font-size: 32px;
                        font-weight: bold;
                        color: #667eea;
                        letter-spacing: 8px;
                        margin: 10px 0;
                    }}
                    .otp-text {{
                        color: #666;
                        font-size: 14px;
                        margin-top: 10px;
                    }}
                    .instructions {{
                        background-color: #fff3cd;
                        border: 1px solid #ffeaa7;
                        border-radius: 6px;
                        padding: 15px;
                        margin: 20px 0;
                        color: #856404;
                    }}
                    .footer {{
                        background-color: #f8f9fa;
                        padding: 20px;
                        text-align: center;
                        color: #666;
                        font-size: 14px;
                        border-top: 1px solid #e9ecef;
                    }}
                    .warning {{
                        color: #dc3545;
                        font-size: 14px;
                        margin-top: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎯 RifleAxis</h1>
                        <p>Password Reset Request</p>
                    </div>
                    
                    <div class="content">
                        <div class="greeting">
                            Hello {user_name},
                        </div>
                        
                        <p>You have requested to reset your password for your RifleAxis account. Use the verification code below to proceed:</p>
                        
                        <div class="otp-container">
                            <div class="otp-code">{otp}</div>
                            <div class="otp-text">Enter this 4-digit code in the app</div>
                        </div>
                        
                        <div class="instructions">
                            <strong>Instructions:</strong>
                            <ul>
                                <li>This code will expire in 10 minutes</li>
                                <li>Enter this code in the RifleAxis app to verify your identity</li>
                                <li>After verification, you'll be able to set a new password</li>
                            </ul>
                        </div>
                        
                        <p>If you didn't request this password reset, please ignore this email and your password will remain unchanged.</p>
                        
                        <div class="warning">
                            <strong>Security Note:</strong> Never share this code with anyone. RifleAxis will never ask for your verification code via phone or email.
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>© 2025 RifleAxis. All rights reserved.</p>
                        <p>This is an automated message, please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            RifleAxis - Password Reset Code
            
            Hello {user_name},
            
            You have requested to reset your password for your RifleAxis account.
            
            Your verification code is: {otp}
            
            This code will expire in 10 minutes.
            
            If you didn't request this password reset, please ignore this email.
            
            © 2025 RifleAxis. All rights reserved.
            """
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html_body,
                body=text_body,
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            logging.error(f"Failed to send password reset email: {str(e)}")
            return False
    
    def send_welcome_email(self, email, user_name):
        """Send welcome email to new users"""
        try:
            subject = "Welcome to RifleAxis! 🎯"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to RifleAxis</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f5f5f5;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: white;
                        border-radius: 12px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 40px 20px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 32px;
                        font-weight: 600;
                    }}
                    .content {{
                        padding: 40px 30px;
                    }}
                    .greeting {{
                        font-size: 20px;
                        margin-bottom: 20px;
                        color: #333;
                    }}
                    .features {{
                        background-color: #f8f9ff;
                        border-radius: 8px;
                        padding: 20px;
                        margin: 20px 0;
                    }}
                    .feature {{
                        margin: 15px 0;
                        padding: 10px 0;
                        border-bottom: 1px solid #eee;
                    }}
                    .feature:last-child {{
                        border-bottom: none;
                    }}
                    .feature h3 {{
                        margin: 0 0 5px 0;
                        color: #667eea;
                    }}
                    .footer {{
                        background-color: #f8f9fa;
                        padding: 20px;
                        text-align: center;
                        color: #666;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎯 Welcome to RifleAxis!</h1>
                        <p>Your precision shooting companion</p>
                    </div>
                    
                    <div class="content">
                        <div class="greeting">
                            Welcome aboard, {user_name}!
                        </div>
                        
                        <p>Thank you for joining RifleAxis, the ultimate platform for precision shooting enthusiasts. We're excited to help you improve your shooting accuracy and track your progress.</p>
                        
                        <div class="features">
                            <h2 style="margin-top: 0; color: #333;">What you can do with RifleAxis:</h2>
                            
                            <div class="feature">
                                <h3>🔫 Manage Your Loadouts</h3>
                                <p>Track your rifles, ammunition, and scopes in one place</p>
                            </div>
                            
                            <div class="feature">
                                <h3>📊 Real-time Training</h3>
                                <p>Monitor cant and acceleration with advanced sensors</p>
                            </div>
                            
                            <div class="feature">
                                <h3>📈 Track Progress</h3>
                                <p>View detailed analytics and improve your shooting performance</p>
                            </div>
                            
                            <div class="feature">
                                <h3>🎯 Ballistic Calculations</h3>
                                <p>Precise calculations for different distances and conditions</p>
                            </div>
                        </div>
                        
                        <p>Ready to get started? Open the RifleAxis app and begin setting up your first loadout!</p>
                    </div>
                    
                    <div class="footer">
                        <p>Happy shooting! 🎯</p>
                        <p>© 2025 RifleAxis. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            Welcome to RifleAxis! 🎯
            
            Hello {user_name},
            
            Thank you for joining RifleAxis, the ultimate platform for precision shooting enthusiasts.
            
            With RifleAxis you can:
            - Manage your rifles, ammunition, and scopes
            - Monitor real-time training data
            - Track your shooting progress
            - Calculate precise ballistics
            
            Ready to get started? Open the RifleAxis app and begin setting up your first loadout!
            
            Happy shooting! 🎯
            © 2025 RifleAxis. All rights reserved.
            """
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html_body,
                body=text_body,
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            logging.error(f"Failed to send welcome email: {str(e)}")
            return False