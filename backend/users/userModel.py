from enum import unique
from flask_login import UserMixin
from backend import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) 
    username = db.Column(db.String(50), unique = True) 
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(20), unique = False) 
    phone_number = db.Column(db.String(10), default = '0000000000') 
    reputation = db.Column(db.Integer(), default = 0)

    decks = db.relationship('Deck', backref = 'user', lazy = True) 
    cards = db.relationship('Card', backref = 'user', lazy = True) 
