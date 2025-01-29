from datetime import datetime, date, timedelta

def get_week_dates():
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    return [start_of_week + timedelta(days=i) for i in range(7)]

def is_due(habit, _date):

    if habit.start_date > _date:
        return False
    elif (_date - habit.start_date).days % habit.days_between_habit == 0:
        return True

def validate_habit_form(name, description, start_date, days_between_habit):
    # Validate input
    if not name:
        return 'Name is required'
    if not days_between_habit.isdigit() and int(days_between_habit)<0:
        return "Intended frequency needs to be a positive integer."
    # Does description or start_date need validating?
    return None

def validate_api_habit_form(name, description, start_date, days_between_habit):
    if not name:
        return 'name: Field is required'
    if not start_date:
        return 'start_date: Field is required'
    if days_between_habit is None:  # Explicit None check
        return 'days_between_habit: Field is required'

    try:
        days_int = int(days_between_habit)
        if days_int <= 0:
            return 'days_between_habit: Must be positive integer'
    except (TypeError, ValueError):
        return 'days_between_habit: Invalid integer format'

    try:
        datetime.strptime(start_date, '%Y-%m-%d').date()

    except ValueError:
        return 'start_date: Invalid date format (YYYY-MM-DD required)'

    return None