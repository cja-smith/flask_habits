from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Habit, DateTracker
from app.utils import validate_habit_form
from datetime import datetime


@app.route('/')
def index():
    habits = Habit.query.all()
    return render_template('index.html', habits=habits)

@app.route('/add_habit', methods=['GET', 'POST'])
def add_habit():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        days_between_habit = request.form['days_between_habit']

        # Validate input
        error = validate_habit_form(name=name,description=description,days_between_habit=days_between_habit)

        if error:
            flash(error)
            return render_template('add_habit.html')

        # Create new habit and date entry
        new_habit = Habit(
            name=name,
            description=description,
            days_between_habit=int(days_between_habit)
        )

        new_entry = DateTracker(
            date=datetime.today().date(),
            habit=new_habit,
            completed=False
        )

        # Add to database
        try:
            db.session.add(new_habit)
            db.session.add(new_entry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}", 500

        return redirect(url_for('index'))

    return render_template('add_habit.html')

@app.route('/edit/<int:habit_id>', methods=['GET', 'POST'])
def edit_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        days_between_habit = request.form['days_between_habit']

        # Validate input
        error = validate_habit_form(name=name, description=description,days_between_habit=days_between_habit)

        if error:
            flash(error)
            return render_template('edit_habit.html')

        habit.name = name
        habit.description = description
        habit.days_between_habit = int(days_between_habit)

        # Commit to database
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}", 500

        return redirect(url_for('index'))

    return render_template('edit_habit.html', habit=habit)
