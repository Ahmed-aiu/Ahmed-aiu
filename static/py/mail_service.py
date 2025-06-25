import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app
import os


def send_email(receiver,topic,text):
    # SMTP server configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER')  
    SMTP_PORT = os.getenv('SMTP_PORT')  
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')  
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD') 
    
    #logger initialization
    logger = current_app.logger
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = 'EU_genaihub@fev.com'
    msg['To'] = receiver
    msg['Subject'] = topic
    msg.attach(MIMEText(text, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Send the email
        server.sendmail('EU_genaihub@fev.com', receiver, msg.as_string())
        logger.info(F"Email successfully sent to {receiver}")
        
    except Exception as e:
        logger.error(F"Failed to send email to {receiver}:{e}")
        
    finally:
        server.quit()