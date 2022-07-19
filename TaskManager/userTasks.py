from flask import render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import * 
import base64
from TaskManager import celery, SENDGRID_API_KEY
import os
from backend import * 

@celery.task #sending welcome email 
def welcome(userObj): 

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'templates', 'welcome.html') 
    email = userObj['email'] 
    name = userObj['username'] 
    with app.app_context(): 
        user = {name:name, email:email}
        output = render_template('welcome.html', user = user) 

    message = Mail(
        from_email='kartflix18@gmail.com', 
        to_emails=email, 
        subject = f'Hey {name}! Welcome to flask-hearts', 
        html_content=output
    )

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message) 
    print(response.status_code, response.body, response.headers) 
