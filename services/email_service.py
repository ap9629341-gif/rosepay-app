"""
Email notification service.

WHAT THIS FILE DOES:
- Sends email notifications for transactions
- Can send emails when money is added, transferred, etc.
- Uses SMTP (Simple Mail Transfer Protocol) to send emails

LEARN:
- SMTP = protocol for sending emails
- We'll use Gmail's SMTP server (smtp.gmail.com)
- For production, you'd use services like SendGrid, AWS SES, etc.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from config import settings


def send_email(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None
) -> bool:
    """
    Send an email.
    
    WHAT IT DOES:
    1. Connects to SMTP server (Gmail)
    2. Creates email message
    3. Sends email
    4. Returns True if successful, False if failed
    
    PARAMETERS:
    - to_email: Who to send to
    - subject: Email subject line
    - body: Plain text email body
    - html_body: Optional HTML version (prettier)
    """
    # If email settings not configured, just print (for development)
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print(f"📧 [EMAIL] Would send to {to_email}: {subject}")
        print(f"   Body: {body}")
        return True  # Return True so app doesn't break
    
    try:
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add plain text version
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML version if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Connect to SMTP server and send
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()  # Enable encryption
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False


def send_transaction_notification(
    user_email: str,
    transaction_type: str,
    amount: float,
    description: str,
    balance: float
) -> bool:
    """
    Send transaction notification email.
    
    WHAT IT DOES:
    1. Creates a nice email message
    2. Includes transaction details
    3. Shows new balance
    4. Sends to user
    
    EXAMPLE:
    When you add $50, user gets email:
    "You received $50.00. New balance: $150.00"
    """
    # Create email subject
    if transaction_type == "deposit":
        subject = f"💰 Money Added to Your Wallet - ${amount:.2f}"
    elif transaction_type == "transfer":
        subject = f"💸 Money Transferred - ${amount:.2f}"
    elif transaction_type == "payment":
        subject = f"💳 Payment Processed - ${amount:.2f}"
    else:
        subject = f"📊 Transaction Update - ${amount:.2f}"
    
    # Create email body (plain text)
    body = f"""
Hello!

Your transaction has been completed:

Type: {transaction_type.title()}
Amount: ${amount:.2f}
Description: {description}
New Balance: ${balance:.2f}

Thank you for using RosePay!
    """.strip()
    
    # Create HTML version (prettier)
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #4CAF50;">Transaction Completed</h2>
        <p>Your transaction has been processed successfully.</p>
        <table style="border-collapse: collapse; width: 100%;">
          <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Type:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{transaction_type.title()}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Amount:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">${amount:.2f}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Description:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{description}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>New Balance:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd; color: #4CAF50; font-weight: bold;">${balance:.2f}</td>
          </tr>
        </table>
        <p>Thank you for using RosePay!</p>
      </body>
    </html>
    """
    
    return send_email(user_email, subject, body, html_body)
