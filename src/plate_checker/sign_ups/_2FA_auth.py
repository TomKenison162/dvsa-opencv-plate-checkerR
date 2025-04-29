import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_code_via_email(email_address, code):
    
    

    # Your email configuration      
    sender_email = 'test.sender.cs.project@gmail.com'
    sender_password = 'znaj xoxc vpdy wonc'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Create message
    subject = 'Verification Code'
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email_address
    message['Subject'] = subject

    # Add code to the email body
    body = f'Your verification code is: {code}'
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email_address, message.as_string())
        print('Code sent successfully.')
    except Exception as e:
        print(f'Error sending code: {e}')


