from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from yargs import parse


settings = parse('settings')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.dburl
db = SQLAlchemy(app)
