from backend import app, login_manager, api, db 
from flask_login import login_required, login_user, logout_user, current_user 
from backend.flashcards import Card, Deck
from flask_restful import Resource
from flask import jsonify, request, make_response, send_from_directory, render_template, send_file
from tasks import *
# from backend.flashcards.file_management.tasks import csvify, htmlify
import numpy as np 
import pandas as pd
import os


class csv(Resource): #flashcards/csv/<did>

    def get(self, did): 
        """
        Asynchornously returns text with csv formatting
        Format: 
            S.no, Front, Back
            1, text, text...
        201 if user isn't logged in or tries to access other deck
        """
        deck = Deck.query.filter_by(id = did).first() 

        if not current_user.id == deck.user_id or \
            not current_user.is_authenticated or \
            not deck: 
            return make_response(jsonify({"error" : "Invalid credentials"}), 201 )
        
        
        cards = Card.query.filter_by(deck_id = deck.id)
        # data = np.array(['Front', 'Back']) # don't need this since adding columns in pd df 
        data = []

        for card in cards: 
            data.append([card.front, card.back]) 

        df = pd.DataFrame(data, columns = ['Front', 'Back'])
        res = make_response(df.to_csv(), 200) 
        res.mimetype = "text/plain"

        result = sendCards.delay( did, current_user.id,csv = df.to_csv(), html = None)
        print(result.status)

        return res     


class html(Resource): #flashcards/html/<did> 

    def get(self, did): 
        """
        Asynchronously returns a text with html formatting
        Looks like 2 cards stacked beside each other
        201 if user isn't logged in or tries to access other deck"""

        deck = Deck.query.filter_by(id = did).first() 

        if not current_user.id == deck.user_id or \
            not current_user.is_authenticated or \
            not deck:
            return make_response(jsonify({"error" : "INvalid credentials"}), 201) 

        
        cards = Card.query.filter_by(deck_id = deck.id)
        data = [] 
        for card in cards: 
            temp = [card.front, card.back] 
            data.append(temp)

        output_from_parsed_template = render_template('base.html', data = data, title = deck.name )
        f = open("./backend/templates/demo.html", "w")
        f.write(output_from_parsed_template)

        result = sendCards.delay( did, current_user.id,None, html = output_from_parsed_template)
        print(result.status) 

        return make_response(output_from_parsed_template)



api.add_resource(csv, '/flashcards/csv/<int:did>')
api.add_resource(html, '/flashcards/html/<int:did>')

