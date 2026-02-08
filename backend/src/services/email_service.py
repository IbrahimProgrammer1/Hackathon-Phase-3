import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os
from urllib.parse import urlencode


class EmailService:
    def __init__(self):
        # For this basic implementation, we'll use environment variables
        # In a real application, you would configure SMTP settings
        self.smtp_server = os.getenv("SMTP_SERVER", "localhost")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("SMTP_FROM_EMAIL", "noreply@todoapp.com")
        self.app_url = os.getenv("APP_URL", "http://localhost:3000")

    def send_password_reset_email(self, to_email: str, reset_token: str) -> bool:
        """
        Send a password reset email to the user.
        For this basic implementation, we'll just print the reset link to console.
        """
        try:
            # Construct the reset link
            reset_url = f"{self.app_url}/auth/reset-password?{urlencode({'token': reset_token})}"

            # For this basic implementation, we'll just print the reset link
            print(f"Password reset link for {to_email}: {reset_url}")

            # In a real application, you would send the email using SMTP
            # The following code shows how it would work:
            '''
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = "Password Reset Request"

            body = f"""
            You have requested to reset your password. Click the link below to reset your password:

            {reset_url}

            If you did not request this, please ignore this email.

            This link will expire in 1 hour.
            """

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            '''

            # For this basic implementation, we'll just print the reset link to console
            # so developers can see it during testing
            print(f"\n--- PASSWORD RESET INSTRUCTIONS ---")
            print(f"Password reset requested for: {to_email}")
            print(f"Reset URL: {reset_url}")
            print(f"--- END PASSWORD RESET INSTRUCTIONS ---\n")

            # In a real application, you would send the email using SMTP
            # The following code shows how it would work:
            """
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            """

            # For now, we'll return True to indicate success
            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False


# Singleton instance
email_service = EmailService()