from celery import Celery 
celery = Celery('TaskManager', broker='redis://localhost:6379', backend = 'redis://localhost:6380') 
SENDGRID_API_KEY = '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'

from TaskManager.beatConfig import *
from TaskManager.flashcardTasks import * 
from TaskManager.recurrentTasks import *
from TaskManager.userTasks import *