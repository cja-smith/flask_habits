import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Habit(db.Model):
    id = db.Column(db.integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    days_between_habit = db.Column(db.Integer, nullable=False)
    last_completed = db.Column(db.DateTime)

    def __repr__(self):
        return f'{self.name}'