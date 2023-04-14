import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

TOKEN_FILE_PATH = './token.txt'

with open(TOKEN_FILE_PATH, 'r') as file:
    auth_token = file.read().splitlines()[0]

app = Flask(__name__)
app.config['VK_AUTH_TOKEN'] = auth_token
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///application_database.db')
db = SQLAlchemy(app)

if not os.path.exists('application_database.db'):
    db.create_all()
    db.session.commit()

from app import routes, models