from pydoc import plain
from celery import Celery
from backend.flashcards import *
import pandas as pd 
from backend import db, app
import datetime
from werkzeug.utils import secure_filename
from flask import render_template
from backend import * #to avoid circular imports
import os
from celery.schedules import crontab 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import * 
import base64
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt 

celery = Celery('tasks', broker='redis://localhost:6379', backend = 'redis://localhost:6380') 
SENDGRID_API_KEY = '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'
#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

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=9, minute=0, day_of_week='*'), #updating history files every day
        # 10.0, #for testing purposes  
        updateHistory.s() 
    )
    sender.add_periodic_task(
        crontab(hour=12, minute=30, day_of_week='*'), #checking for non-revisers every day
        # 30.0, #for testing purposes
        reviseCheck.s()
    )
    sender.add_periodic_task(
        crontab(minute = 30, hour = 12, day_of_month=0), #generating monthly report once a month 
        # 100.0,#for testing purposes
        monthlyReport.s()
    )


@celery.task
def monthlyReport(): 
    users =User.query.all()
    for user in users: 
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'history', str(user.id))
        try:
            df = pd.read_csv(filepath) 
            # datetime, no decks, no cards, avg score, rep

            X = df.iloc[:, 0] #datetime col
            dcount  = df.iloc[:,1] 
            ccount = df.iloc[:,2] 
            avg = df.iloc[:,3]
            rep = df.iloc[:,4]
            plt.plot(X, dcount, color='r', label='Decks') 
            plt.plot(X, ccount, color='b', label='Cards') 
            plt.plot(X, avg, color = 'g', label = 'Average Score') 
            plt.plot(X, rep, color='c', label = 'Reputation')
            plt.xlabel("Date") 
            plt.ylabel("Magnitude") 
            plt.title(f'Monthly report - {user.username}')
            plt.legend() 
            filename = filepath+ '.pdf'
            plt.savefig(filename, format='pdf')

            #sending picture as email 
            with app.app_context(): 
                output = render_template('report.html', name = user.username, score = user.reputation, filepath = f'../history/{user.id}.pdf')

                message = Mail(
                    from_email = '21f1003074@student.onlinedegree.iitm.ac.in',
                    to_emails=user.email, 
                    subject = f'Hey {user.username}! Here are your stats', 
                    html_content=output
                )
                
                with open(filename, 'rb') as f: 
                    data = f.read() 
                encoded_output = base64.b64encode(data).decode()

                attachedFile = Attachment(
                    FileContent(encoded_output), 
                    FileName('Monthly Report'), 
                    FileType('application/pdf'), 
                    Disposition('attachment')
                )
                message.attachment = attachedFile

                sg = SendGridAPIClient(SENDGRID_API_KEY) 
                response = sg.send(message) 
                print(response.status_code, response.body, response.headers)

            plt.clf() #so that multiple graphs don't overlay

        #if users history hasn't been made yet don't crash 
        except Exception as e: 
            print(e) 
            continue

        #creating the accumulated graph
    return 


@celery.task 
def reviseCheck(delt = 86400): #del corresponds to maximum allowable diff in time (seconds) 
    users = User.query.all()
    current_time = datetime.datetime.now() 
    for user in users: 
        decks = Deck.query.filter_by(user_id = user.id)
        last_seen = decks[0].last_seen
        seconds_passed = (current_time - last_seen).total_seconds()
        if seconds_passed > delt: 
            print('Bad User: ' , user.username, user.email)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'templates', 'revise.html')
            output = ''
            with app.app_context():
                output = render_template('revise.html', name = user.username, score = user.reputation)

            message = Mail(
                from_email = '21f1003074@student.onlinedegree.iitm.ac.in',
                to_emails=user.email, 
                subject = f'Hey {user.username}! How about a study session', 
                html_content=output
            )

            sg = SendGridAPIClient(SENDGRID_API_KEY) 
            response = sg.send(message) 
            print(response.status_code, response.body, response.headers)



@celery.task
def updateHistory(): # datetime, no decks, no cards, avg score, rep | and same for other categories 
    for user in User.query.all(): 
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'history') 
        filepath = os.path.join(filepath, str(user.id))
        file = open(filepath, 'a' ) 
        dcount = Deck.query.filter_by(user_id = user.id).count() 
        ccount = Card.query.filter_by(user_id = user.id).count()
        s=0
        for deck in Deck.query.filter_by(user_id = user.id):
            s += deck.score

        avg = s/dcount 
        file.write(f'{datetime.datetime.now()}, {dcount}, {ccount}, {avg}, {user.reputation}\n')
        file.close() 


@celery.task #handling import for cards
def addCards(filename, uid): 
    
    #reading the upload folder as df to be able to add cards to new deck 
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'templates', str(uid))
    file = open(file_path, 'r') 
    lines = file.readlines() 
    values = []

    for line in lines:
        if line == lines[0]: 
            continue #we don't want the headers

        l = line.strip() 
        print(l)  
        f, b = l.split(', ')
        values.append([f, b])
    print(values) 
    last_seen = datetime.datetime.now()
    deck = Deck(
        name = filename, 
        description = "Imported Deck", 
        last_seen = last_seen, 
        user_id = uid
    )
    db.session.add(deck)
    db.session.commit() 
    did = Deck.query.filter((Deck.user_id == uid) & (Deck.last_seen == last_seen)).first().id 
    for row in values: #making each card and committing
        front, back = row[0], row[1] 
        card = Card(
            front = front, 
            back = back, 
            deck_id = did, 
            user_id = uid
        )

        db.session.add(card) 
        db.session.commit() 
    db.session.commit()
    return 


@celery.task #handling exports, being sent to emails
def sendCards(did, uid, csv = None, html = None):
    user = User.query.filter_by(id = uid).first() 
    deck = Deck.query.filter_by(id = did).first()
    message = Mail(
        from_email = '21f1003074@student.onlinedegree.iitm.ac.in',
        to_emails = user.email,
        subject = f'Exporting {deck.name} as a csv and html file', 
        plain_text_content='Please find below the attachments of the deck in the formats of csv and html', 
    )

    data = csv if csv else html
    encoded_output = base64.b64encode(data.encode("ascii")).decode() 
    filename = f'{deck.name}.csv' if csv else f'{deck.name}.html'

    attachedFile = Attachment(
        FileContent(encoded_output), 
        FileName(filename), 
        FileType('text/html'), 
        Disposition('attachment')
    )

    message.attachment = attachedFile 

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)
