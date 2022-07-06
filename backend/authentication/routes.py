from backend import app, api, db, login_manager, load_user
from flask_login import login_required, login_user, logout_user, current_user
from backend.users.userModel import User 
from flask import jsonify, request, make_response
from flask_restful import Resource

class login(Resource): 

    def post(self): 
        """
        Takes in the email, username and password information
        If username doesn't exist or password doesn't match returns 404
        """
        data = request.get_json() 
        user = User.query.filter_by(username = data['username']).first() 
        if user: 
            #checking if passwords match
            if user.password == data['password']:                
                login_user(user) 
                return make_response(jsonify({"msg": "Login succesfull", "uid" : user.id}), 200) 
            else:
                return make_response(jsonify({"error":"Passwords don't match"}), 404)
            
        #if the user with that username doesn't exist 
        else: 
            return make_response(jsonify({"error":"User doesn't exist"}), 404)

class logout(Resource):
    """
    Sending a get or a post request logs out the current user
    """
    @login_required
    def get(self): 
        logout_user()
        return make_response(jsonify({"msg": "Logout succesfull"}), 200)
    
    def post(self): 
        logout_user()
        return make_response(jsonify({"msg": "Logout succesfull"}), 200)


api.add_resource(login, '/login')
api.add_resource(logout, '/logout') 
