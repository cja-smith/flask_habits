from datetime import datetime,timezone
from email.policy import default

from app import db

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    date_created = db.Column(db.Date, default=datetime.now(timezone.utc).date())
    start_date = db.Column(db.Date, nullable=False)
    days_between_habit = db.Column(db.Integer, nullable=False, default=1)
    dates = db.relationship('DateTracker', backref='habit', lazy=True, cascade='all, delete')

    def __repr__(self):
        return f'{self.name}'

class DateTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'))
    completed = db.Column(db.Boolean, default=False)