# FLASK-HEARTS

This is the project which was created for MAD-II IITM. 
Author: Akhilesh Kaushik Valluri
Roll No: 21f1003074

## Requirements
* Flask 
* Flask - CORS
* Flask - RESTful
* Flask - SQL Alchemy
* JWT
* Jinja-2
* Matplotlib, Numpy, Pandas
* Vue JS - CLI 
* Vuex
* Redis
* Celery, Celery-Beat, Celery[Redis] 

Make sure all the above are installed along with dependencies.  

## How to run the application

1) Go to root directory of project folder. i.e when 'ls' is typed make sure you can see 'run.py', 'backend', 'frontend' etc
```
    ls
    >>> run.py backend frontend Taskmanager
```
2) Start a python instance and run the following commands
 ```
    python3 
    from backend import db 
    db.drop_all() 
    db.create_all() 
    exit()
```
3) Run 'run.py'. This will start the flask server 
```
    python run.py
```
4) Create two redis servers, on ports: 6379 and 6380. (redis-server --port <port-number>)
```
    redis-server
    redis-server --port 6380
```
5) Start the celery instance in TaskManager. 
```
    celery -A TaskManager.celery -l INFO
```
6) Start the beat service
```
    celery -A TaskManager.celery beat 
```
7) cd into directory: 'frontend' (cd frontend)
```
    cd frontend
```
8) Start the vue application using npm (npm run serve) 
```
    npm run serve 
```
9) Navigate to [localhost]('http://localhost:8080')
10) Navigate through the application and enjoy 