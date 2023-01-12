from flask import Blueprint, render_template, session
from app.models import User, Tag, Salary, ActiveSalary, MonthlyCharge, ExpiredCharges
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
        # Change this query to just getting monthly charges to display on 'monthly charges'
        monthly_charges = db.query(MonthlyCharge.time_created, MonthlyCharge.amount, MonthlyCharge.description, Tag.tag_name, Tag.id, MonthlyCharge.id, MonthlyCharge.start_date
            ).filter(MonthlyCharge.user_id == user_id
            ).join(Tag
            ).all()
        
        expired_charges = db.query(ExpiredCharges.time_created, ExpiredCharges.amount, 
            ExpiredCharges.description, Tag.tag_name, Tag.id, ExpiredCharges.id, ExpiredCharges.start_date, ExpiredCharges.expiration_limit, ExpiredCharges.start_date
        ).filter(ExpiredCharges.user_id == session['user_id']
        ).join(Tag
        ).all()

    except Exception as e:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    return render_template('profile.html',
        user_data=user_data, 
        all_salaries=all_salaries,
        active_salary=active_salary,
        loggedIn=is_loggedin,
        tags = allTags, 
        today=today,
        all_inactive_categories=all_inactive_categories,
        monthly_charges=monthly_charges, 
        expired_charges=expired_charges
    )

@bp.route('/edit-all-salaries')
def edit_all_salaries():
    db = start_db_session()
    user_id = session['user_id']
    if user_id:
        loggedIn=True
    else:
        user_id=False
    try:
        all_salaries = db.query(Salary).filter(Salary.user_id == user_id).all()
        all_tags = (
            db.query(Tag)
            .filter(Tag.user_id == user_id)
            .filter(Tag.active == True)
            .all()
        )
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    return render_template('all-salaries.html', all_salaries=all_salaries, tags=all_tags, today=today ,loggedIn=loggedIn)