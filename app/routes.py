from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import Habit, DateTracker
from app.utils import validate_habit_form
from datetime import datetime, date, timedelta


@app.route('/')
def index():
    habits = Habit.query.all()
    return render_template('index.html', habits=habits)


# Add form submission logic for checkbox updates !
@app.route('/week', methods=['GET', 'POST'])
def week():
    # Calculate start of week (Monday)
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    habits = Habit.query.all()

    def is_due(habit, _date):

        if habit.start_date > _date:
            return False
        elif (_date - habit.start_date).days % habit.days_between_habit == 0:
            return True

    completions = {(tracker.habit_id, tracker.date):
                       tracker.completed
                   for tracker in DateTracker.query.filter(
            DateTracker.date.between(week_dates[0], week_dates[-1])
        ).all()}

    return render_template('week.html',
                           str_start_of_week=start_of_week.strftime('%m/%d/%Y'),
                           week_dates=week_dates,
                           habits=habits,
                           completions=completions,
                           is_due=is_due)


@app.route('/add_habit', methods=['GET', 'POST'])
def add_habit():
    today = date.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        start_date = request.form['start_date']
        days_between_habit = request.form['days_between_habit']

        # Validate input
        error = validate_habit_form(name=name,
                                    description=description,
                                    days_between_habit=days_between_habit,
                                    start_date=start_date)

        if error:
            flash(error)
            return render_template('add_habit.html')

        # Create new habit and date entry
        new_habit = Habit(
            name=name,
            description=description,
            start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
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

    return render_template('add_habit.html', today=today)

@app.route('/edit/<int:habit_id>', methods=['GET', 'POST'])
def edit_habit(habit_id):
    today = date.today().strftime('%Y-%m-%d')
    habit = Habit.query.get_or_404(habit_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        start_date = request.form['start_date']
        days_between_habit = request.form['days_between_habit']

        # Validate input
        error = validate_habit_form(name=name,
                                    description=description,
                                    days_between_habit=days_between_habit,
                                    start_date=start_date)

        if error:
            flash(error)
            return render_template('edit_habit.html')

        habit.name = name
        habit.description = description
        habit.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        habit.days_between_habit = int(days_between_habit)

        # Commit to database
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}", 500

        return redirect(url_for('index'))

    return render_template('edit_habit.html', habit=habit, today=today)

@app.route('/delete/<int:habit_id>', methods=['POST'])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    try:
        db.session.delete(habit)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting habit: {str(e)}", "error")
        return render_template('edit_habit.html', habit=habit)

    return redirect(url_for('index'))
