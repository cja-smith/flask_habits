from datetime import datetime,timezone
from app import db

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.date(datetime.now(timezone.utc)))
    days_between_habit = db.Column(db.Integer, nullable=False, default=1)
    dates = db.relationship('DateTracker', backref='habit', lazy=True)

    def __repr__(self):
        return f'{self.name}'

class DateTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'))
    completed = db.Column(db.Boolean, default=False)