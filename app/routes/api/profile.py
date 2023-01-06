from flask import Blueprint, request, session, redirect, render_template
from app.models import User, Salary, ActiveSalary
from app.db import start_db_session

bp = Blueprint('api/profile', __name__, url_prefix='/api')


# Update user name
@bp.route('/update-username', methods=['POST'])
def update_user_name():
    data = request.form
    db = start_db_session()
    try:
        user_data = db.query(User).filter(User.id == session['user_id']).one()
        user_data.username = data['new_username'].strip()

        db.commit()
    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    return redirect(request.referrer)


# Add new Active Salary
@bp.route('/add-salary', methods=['POST'])
def add_salary():
    data = request.form
    user_id = session['user_id']
    new_salary_start_date = data['new-salary-date']
    salary_start = int(new_salary_start_date.split('-')[0] + new_salary_start_date.split('-')[1])
    db = start_db_session()
    try:
        # Check to see if they already have an active salary. 
        old_salary = db.query(ActiveSalary).filter(ActiveSalary.user_id == user_id).first()
        # If so, make a new non active salary with old data. 
        if old_salary:
        # Need to create last date which is one less than the start date of new active salary
            # the end date of the new expired charged needs to be 'salary_start' minus 1
            old_salary_end_date = salary_start - 1
            # need to check for double zeros in the end, if so, subtract year and make month 12
            if old_salary_end_date % 100 == 0:
                old_salary_end_date = int(str(int(new_salary_start_date.split('-')[0]) - 1) + '12')
            # Make new expired salary
            expired_salary = Salary(
                salary_amount = old_salary.salary_amount,
                user_id = user_id,
                start_date = old_salary.start_date,
                last_payment = old_salary_end_date
            )
            db.add(expired_salary)
            db.commit()

            # Update active salary data with form data
            old_salary.salary_amount = data['new-monthly-income']
            old_salary.start_date = salary_start
            db.commit()
        else: 
            new_active = ActiveSalary(
                salary_amount = data['new-monthly-income'],
                user_id = user_id,
                start_date = salary_start
            )
            db.add(new_active)
            db.commit()
    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Income not added.")
    return redirect(request.referrer)

# stop active salary
@bp.route('/stop-active-salary', methods=['POST'])
def stop_user_salary():
    data = request.form
    db = start_db_session()
    salary_id = data['salary-id']
    expiration_date = data['expiration-limit-date']
    salary_end_date = int(expiration_date.split('-')[0] + expiration_date.split('-')[1])

    try:
        old_salary = db.query(ActiveSalary).filter(ActiveSalary.id == salary_id).one()
        new_expired_salary = Salary (
            salary_amount = old_salary.salary_amount,
            start_date = old_salary.start_date,
            last_payment = salary_end_date,
            user_id = session['user_id']
        )
        db.add(new_expired_salary)
        db.delete(old_salary)
        db.commit()
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    return redirect(request.referrer)


# Delete Salary
@bp.route('/delete-user-salary', methods=['POST'])
def delete_user_salary():
    data = request.form
    db = start_db_session()
    salary_id = data['salary-id']
    try:
        if 'salary-is-active-delete' in data:
            db.query(ActiveSalary).filter(ActiveSalary.id == salary_id).delete()
            db.commit()
        else:
            db.query(Salary).filter(Salary.id == salary_id).delete()
            db.commit()
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    return redirect(request.referrer)


# Update Active user salary
@bp.route('/edit-user-active-salary', methods=['POST'])
def edit_user_active_salary():
    data = request.form
    db = start_db_session()
    user_id = session['user_id']
    new_salary_start = int(data['active-salary-start-date-edit'].split('-')[0] + data['active-salary-start-date-edit'].split('-')[1])
    new_monthly_income = data['new-active-monthly-income']

    try:
        salary_to_update = db.query(ActiveSalary).filter(ActiveSalary.user_id == user_id).one()
        salary_to_update.start_date = new_salary_start
        salary_to_update.salary_amount = new_monthly_income
        db.commit()

    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    return redirect(request.referrer)
    
# Update old user salary
@bp.route('/edit-user-old-salary', methods=['POST'])
def edit_user_old_salary():
    data = request.form
    db = start_db_session()
    new_salary_start = int(data['salary-start-date-edit'].split('-')[0] + data['salary-start-date-edit'].split('-')[1])
    new_salary_end = int(data['salary-end-date-edit'].split('-')[0] + data['salary-end-date-edit'].split('-')[1])
    salary_id = data['salary-id-edit']
    new_monthly_income = data['edit-salary-income']

    try:
        salary_to_update = db.query(Salary).filter(Salary.id == salary_id).one()
        salary_to_update.start_date = new_salary_start
        salary_to_update.last_payment = new_salary_end
        salary_to_update.salary_amount = new_monthly_income
        db.commit()

    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    return redirect(request.referrer)