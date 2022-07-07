import json
from flask import jsonify, request, make_response
from flask_restful import Resource
from backend.notes.noteModel import Notebook, Page 
from flask_login import current_user
from backend import api, db
import datetime 

class allNotes(Resource): 

    def get(self): 
        """
        Returns all the Notes formatted in the following way: 
            id
            name
            colour
            description
            created
            user_id     
        """
        notebooks = Notebook.query.all()
        output = []
        for notebook in notebooks: 
            notebookObj  = {
                'id' : notebook.id, 
                'name' : notebook.name, 
                'colour' : notebook.colour, 
                'description' : notebook.description, 
                'created' : notebook.created, 
                'user_id' : notebook.user_id
            }

            output.append(notebookObj) 

        return make_response(jsonify(output), 200) 
        
    
    def post(self): 
        """
        Creates a new notebook which checks for the necessary information, else sets deafults.
        User must be logged in to post
        200 for ok, 201 for error
        """
        if not current_user.is_authenticated:
            return make_response(jsonify({"error" : "Please log in"}))

        data = request.get_json() 

        try :  
            name = data['name']
            colour = 'white'
            if 'colour' in data.keys(): 
                colour = data['colour']
            description = '' 
            if 'description' in data.keys(): 
                description = data['description'] 
            created = datetime.datetime.now() 
            last_seen = created 
            user_id = current_user.id

            notebook = Notebook(
                name = name, 
                colour = colour, 
                description = description,
                created = created, 
                last_seen = last_seen,
                user_id = user_id)
            
            db.session.add(notebook) 
            db.session.commit() 

            return make_response(jsonify({"msg" : "Notebook succesfully created"}), 200) 
        
        except Exception as e: 
            return make_response(jsonify({"msg" : f'You have not given all information. Error : {e}'}), 201)


class singleNote(Resource): 
    
    def get(self, nid): 
        """
        Returns specific notebook with id
        Returns 201 if doesn't exist"""

        notebook = Notebook.query.filter_by(id = nid).first() 

        if not notebook: 
            return make_response(jsonify({'error' : 'Notebook does note exist'}), 201) 
        
        notebookObj = {
            'id' : notebook.id, 
            'name' : notebook.name, 
            'colour' : notebook.colour, 
            'description' : notebook.description, 
            'created' : notebook.created, 
            'last_seen' : notebook.last_seen, 
            'user_id' : notebook.user_id
        }

        return make_response(jsonify(notebookObj), 200) 

    def delete(self, nid): 
        """
        Deletes notebook and it's pages
        Checks if user is logged in
        201 if any error (including user not logged in, notebook not found) """

        if not current_user.is_authenticated: 
            return make_response(jsonify({"error" : "please log in"}), 201) 

        notebook = Notebook.query.filter_by(id = nid).first() 

        if not notebook.user_id == current_user.id or not notebook: 
            return make_response(jsonify({"error" : "Please log in as notebook user"}), 201)
        
        Notebook.query.filter_by(id = nid).delete()
        Page.query.filter_by(notebook_id = nid).delete()
        db.session.commit() 

        return 200 
    
    def patch(self, nid): 
        """Updates notebook without strict key checking
        user should be logged in
        201 if error"""

        notebook = Notebook.query.filter_by(id = nid ).first() 

        if not current_user.is_authenticated or\
            not current_user.id == notebook.user_id or\
            not notebook: 
            return make_response(jsonify({"error" : "Please log in"}), 201)
        
        data = request.get_json()

        if 'name' in data.keys(): 
            notebook.name = data['name']

        if 'colour' in data.keys(): 
            notebook.colour = data['colour']

        if 'description' in data.keys(): 
            notebook.description = data['description']
        
        notebook.last_seen = datetime.datetime.now() 
        db.session.commit() 

        return 200 

class userNotes(Resource): 

    def get(self): 
        """Returns all teh notebooks for the currently logged in user
        200 if ok
        201 else"""

        try: 
            if not current_user.is_authenticated: 
                return make_response(jsonify({"error" : "please log in"}), 201)
            notebooks = Notebook.query.filter_by(user_id = current_user.id ) 
            output = [] 
            
            for notebook in notebooks: 
                notebookObj = {
                    'id' : notebook.id,
                    'name' : notebook.name,
                    'colour' : notebook.colour, 
                    'description' : notebook.description, 
                    'last_seen' : notebook.last_seen
                }
                output.append(notebookObj)
            
            return make_response(jsonify(output), 200) 

        except Exception as e: 
            return make_response(jsonify({"error" : f'Unable to process request. Error : {e}'}), 201)
        
api.add_resource(userNotes, '/user/notebook') 
api.add_resource(allNotes, '/notebook')
api.add_resource(singleNote, '/notebook/<int:nid>') 
