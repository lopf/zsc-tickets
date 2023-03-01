import os
import logging
import json
import smtplib
from email.mime.text import MIMEText

import azure.functions as func

def send_email(to_email, body):
    # Login to your Gmail account
    from_email = os.environ.get('GMAIL_USERNAME') # replace with your Gmail email address
    password = os.environ.get('GMAIL_PASSWORD') # replace with your Gmail password

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)

    # Create message
    message = MIMEText(body)
    message['Subject'] = 'New Queue Message'
    message['From'] = from_email
    message['To'] = to_email

    # Send email
    server.send_message(message)
    server.quit()

def main(msg: func.QueueMessage):
    logging.info('Python queue trigger function processed a queue item.')

    result = json.dumps({
        'id': msg.id,
        'body': msg.get_body().decode('utf-8'),
        'expiration_time': (msg.expiration_time.isoformat()
                            if msg.expiration_time else None),
        'insertion_time': (msg.insertion_time.isoformat()
                           if msg.insertion_time else None),
        'time_next_visible': (msg.time_next_visible.isoformat()
                              if msg.time_next_visible else None),
        'pop_receipt': msg.pop_receipt,
        'dequeue_count': msg.dequeue_count
    })

    logging.info(result)

    # Send email notification
    to_email = os.environ.get('NOTIFICATION_EMAIL') # replace with recipient email address
    #body = "New Queue Message:\n" + result.toString()
    body = "New Queue Message:\n" + result

    send_email(to_email, body)
