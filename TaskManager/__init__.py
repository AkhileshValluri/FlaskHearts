from celery import Celery 
celery = Celery('TaskManager', broker='redis://localhost:6379', backend = 'redis://localhost:6380') 
SENDGRID_API_KEY = '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'

from TaskManager.beatConfig import *
from TaskManager.flashcardTasks import * 
from TaskManager.recurrentTasks import *