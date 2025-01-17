from app.__init__ import app, db
from app.models import Habit, DateTracker

with app.app_context():
    db.create_all()