# API_YATUBE
## Description
A simple api intended for social network "yatube"

## Installation
### Clone the project from github:
'git clone git@github.com:klinf1/api_final_yatube.git'
### Go to the the repository
'cd api_final_yatube'
### Create and start virtual environment
'python -m venv venv'
'source venv/Scripts/activate'
### Install requirements from requirements.txt
'pip install -r requirements.txt'
### Create and apply migrations
'python manage.py makemigrations'
'python manage.py migrate'
### Start the app
'python manage.py runserver'

## Some examples
### Getting all posts
'http://127.0.0.1:8000/api/v1/posts'
This also supports limit-offset pagination
### Getting information about a group
'http://127.0.0.1:8000/api/v1/groups/{group_id}'