from flask import Flask, session
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api 

app = Flask(__name__, instance_relative_config = True) 
app.config.from_object('backend.config.DefaultConfig')
app.secret_key = 'secret_key' #secret key for sessions

api = Api(app) 

db = SQLAlchemy(app) 

login_manager = LoginManager()
login_manager.init_app(app)

#used to return information from user object later on in the app
#Will use the userobject.property to verify login later on 
@login_manager.user_loader 
def load_user(user_id):
    return User.query.filter_by(id = int(user_id)).first()

#importing api routes | not necessary, jic
from backend.flashcards import deckRoutes, cardRoutes, file_management
from backend.users import userRoutes
from backend.authentication import routes
from backend.notes import pageRoutes, notebookRoutes
from backend.quizzes import questionRoutes, optionRoutes, quizRoutes

#importing models
from backend.flashcards import Deck, Card
from backend.users.userModel import User
from backend.notes import Notebook, Page
from backend.quizzes import Quiz, Question, Option