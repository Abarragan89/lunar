from flask import Blueprint, render_template, session
from app.models import User, Tag, Salary, ActiveSalary
from app.db import start_db_session
import datetime


today = datetime.datetime.now()

# Create Blueprint
bp = Blueprint('site_profile', __name__)


@bp.route('/profile')
def profile():
    db = start_db_session()
    user_id = session.get('user_id')
    is_loggedin = session.get('loggedIn')

    try:
        user_data = db.query(User).filter(User.id == session['user_id']).one()
        all_salaries = db.query(Salary).filter(Salary.user_id == user_id).all()
        active_salary = db.query(ActiveSalary).filter(ActiveSalary.user_id == user_id).first()

        if active_salary:
            all_salaries.insert(0, active_salary)

        allTags = (
            db.query(Tag)
            .filter(Tag.user_id == user_id)
            .filter(Tag.active == True)
            .all()
        )

        all_inactive_categories = (
            db.query(Tag)
            .filter(Tag.user_id == user_id)
            .filter(Tag.active == False)
            .all()
        )
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    return render_template('profile.html',
        user_data=user_data, 
        all_salaries=all_salaries,
        active_salary=active_salary,
        loggedIn=is_loggedin,
        tags = allTags, 
        today=today,
        all_inactive_categories=all_inactive_categories
    )

@bp.route('/edit-all-salaries')
def edit_all_salaries():
    db = start_db_session()
    user_id = session['user_id']
    try:
        all_salaries = db.query(Salary).filter(Salary.user_id == user_id).all()
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    return render_template('all-salaries.html', all_salaries=all_salaries, today=today)