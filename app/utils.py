from datetime import date, timedelta

def get_week_dates():
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    return [start_of_week + timedelta(days=i) for i in range(7)]

def validate_habit_form(name, description, start_date, days_between_habit):
    # Validate input
    if not name:
        return 'Name is required'
    if not days_between_habit.isdigit() and int(days_between_habit)<0:
        return "Intended frequency needs to be a positive integer."
    # Does description or start_date need validating?
    return None