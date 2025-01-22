from __init__ import app,db
from models import Habit, DateTracker
from flask import render_template, redirect, url_for, request
from datetime import datetime


@app.route('/')
def index():
    habits = Habit.query.all()
    return render_template('index.html', habits=habits)

@app.route('/add_habit', methods=['GET','POST'])
def add_habit():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        days_between_habit = request.form['days_between_habit']

        if not name or not description or not days_between_habit.isdigit():
            return f"Please fill out fields correctly.", 400

        new_habit = Habit(
            name=name,
            description=description,
            days_between_habit=int(days_between_habit)
        )

        new_datetracker_entry= DateTracker(
            date=datetime.today().date(),
            habit=new_habit,
            completed=False
        )
        try:
            db.session.add(new_habit)
            db.session.add(new_datetracker_entry)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return f"Error {str(e)} occurred, please try again.", 500

        return redirect(url_for('index'))
    return render_template('add_habit.html')
