from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from json import load
import os

app = Flask(__name__)

with open('app/config.json', 'r') as config_f:
    config = load(config_f)

app.config['VK_AUTH_TOKEN'] = config['VK_AUTH_TOKEN']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'application_database.db')
db = SQLAlchemy(app)

from app import routes, models

if not os.path.exists('application_database.db'):
    db.create_all()
    db.session.commit()
    print('creating application_database.db')
