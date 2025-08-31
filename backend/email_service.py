import os
import requests

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAIL_FROM_EMAIL = os.getenv("MAIL_FROM_EMAIL")

def send_otp_email(to_email: str, otp: str):
    """Sends a one-time passcode to the specified email using Mailgun."""
    
    if not all([MAILGUN_DOMAIN, MAILGUN_API_KEY, MAIL_FROM_EMAIL]):
        print("Email service is not configured. Check environment variables.")
        # In a real app, raise an error here.
        return None
    
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={"from": f"AetherNotes <{MAIL_FROM_EMAIL}>",
                  "to": [to_email],
                  "subject": "Your AetherNotes Login Code",
                  "text": f"Your one-time login code is: {otp}"})
        
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        print(f"Successfully sent OTP email to {to_email}")
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"Error sending email: {e}")
        return None