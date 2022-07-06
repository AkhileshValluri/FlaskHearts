from backend import api, app 
from flask_login import  current_user 
from flask_restful import Resource
from flask import jsonify, request, make_response
from tasks import *
import pandas as pd
from werkzeug.utils import secure_filename

class imp(Resource): #/flashcards/import

    def post(self): 
        """
        Adds a new deck to the user with the listed cards front and back 
        Accepted file formats: *.csv, *.txt
            front, back
            something, somethignelse...
        The name of the csv will be taken as the name for the deck
        The key for the file SHOULD be 'file'
        Does this asynchronously
        """
        if not current_user.is_authenticated:
            return make_response(jsonify({"error" : "Please log in/give correct data"}), 201)
        
        f = request.files['file'] 
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'templates', str(current_user.id)))
        filename = secure_filename(f.filename)

        if not filename.split('.')[1] in ['csv', 'txt'] or not f: 
            return make_response(jsonify({"msg" : "File type is not correct"}))

        result = addCards.delay(filename, current_user.id)
        print(result.status)
        return make_response(jsonify({"msg" : "Processing file currently"}), 200 )
        

api.add_resource(imp, '/flashcards/import')