from app.__init__ import app,db
from app.models import Habit, DateTracker
from datetime import date

with app.app_context():

    # Clear existing data

    DateTracker.query.delete()
    Habit.query.delete()
    db.session.commit()

    # Create and add test habits
    habit1 = Habit(name='Cardio',
                       description='Testing newly created DB',
                       days_between_habit=2,)

    db.session.add(habit1)
    db.session.commit()

    habit2 = Habit(name='Read',
                       description='Read a chapter of book',
                       days_between_habit=1,)

    db.session.add(habit2)
    db.session.commit()

    # Create and add test date entries
    date1 = DateTracker(date= date.today(),
                            habit=habit1,
                            completed=True)

    db.session.add(date1)
    db.session.commit()

    date2 = DateTracker(date= date.today(),
                            habit=habit2,
                            completed=True)

    date3 = DateTracker(date= date(2025,1,20),
                        habit=habit2,
                        completed=True)

    db.session.add(date2)
    db.session.add(date3)
    db.session.commit()

    # Verify
    print(f'All habits:{Habit.query.all()}')

    for habit in [habit1,habit2]:
        print(f'Current habit: {habit.name}')
        for date_entry in habit.dates:
            print(f'Date:{date_entry.date}, Completed:{date_entry.completed}')