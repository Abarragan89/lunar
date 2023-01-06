from flask import Blueprint, request, jsonify, session, redirect, render_template
from app.models import MonthlyCharge, ExpiredCharges
from app.db import start_db_session

bp = Blueprint('api/charges', __name__, url_prefix='/api')


# Update Monthly Bill (completely change history)
@bp.route('/complete-edit-monthly-charge', methods=['POST'])
def edit_monthly_charge():
    data = request.form
    db = start_db_session()
    monthly_id = data['monthly-id']
    monthly_tag = data['monthly-category']
    monthly_price = data['monthly-price']
    monthly_description = data['monthly-name']
    monthly_start_date = data['monthly-date']
    start_date = int(str(monthly_start_date.split('-')[0]) + str(monthly_start_date.split('-')[1]))

    try:
        db.query(MonthlyCharge).filter(MonthlyCharge.id == monthly_id).update({
            'description': monthly_description.strip(),
            'amount': monthly_price.strip(),
            'user_id': session['user_id'],
            'tag_id': monthly_tag,
            'start_date': start_date,
        })
        db.commit()
    except Exception as e:
        db.rollback()
        return render_template('error-page.html', message="Oops, something happened. Please try again.")
    return redirect(request.referrer)


# Update Monthly Charge (update moving forward)
@bp.route('/update-edit-monthly-charge', methods=['POST'])
def update_monthly_charge():
    data = request.form
    db = start_db_session()
    monthly_id = data['monthly-id']
    monthly_tag = data['monthly-category']
    monthly_price = data['monthly-price'].strip()
    monthly_description = data['monthly-name'].strip()
    monthly_start_date = data['monthly-date']

    # This is the limit that will be placed on the expired charge. Only query less than this in history
    # This will also be the start date of the new monthly charge. From this date forward. greater than or equal to
    new_charge_start_date = int(str(monthly_start_date.split('-')[0]) + str(monthly_start_date.split('-')[1]))

    # the end date of the new expired charged needs to be 'new_charge_start_date' minus 1
    new_expired_end_date = new_charge_start_date - 1
    # need to check for double zeros in the end, if so, subtract year and make month 12
    if new_expired_end_date % 100 == 0:
        new_expired_end_date = int(str(int(monthly_start_date.split('-')[0]) - 1) + '12')

    try:
        # get the data from the old monthly charge to make an expired charge
        expired_monthly = db.query(MonthlyCharge).filter(MonthlyCharge.id == monthly_id).one()
        expiration_date = int(str(expired_monthly.start_date)[:3] + str(expired_monthly.start_date)[3:])
        

        # create new expired monthly based on old monthly charge
        new_expired_monthly = ExpiredCharges(
            description = expired_monthly.description,
            amount = expired_monthly.amount,
            tag_id = expired_monthly.tag_id,
            user_id = session['user_id'],
            expiration_limit = new_expired_end_date,
            start_date = expiration_date
        )
        db.add(new_expired_monthly)
        # delete old monthly charge from table. 
        db.delete(expired_monthly)
        db.commit()

        # create new current monthly charge
        newMonthly = MonthlyCharge(
            description = monthly_description,
            tag_id = monthly_tag,
            user_id = session['user_id'],
            amount = monthly_price,
            start_date = new_charge_start_date
            )
        db.add(newMonthly)
        db.commit()
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops, something happened. Please try again.")
    return redirect(request.referrer)



# Stop Monthly Bill
@bp.route('/stop-monthly-charge', methods=['POST'])
def stop_monthly_charge():
    data = request.form
    db = start_db_session()
    monthly_id = data['monthly-id']
    expiration_limit = data['expiration-limit-date']
    expiration_limit = int(expiration_limit.split('-')[0] + expiration_limit.split('-')[1])

    try:
        expired_monthly = db.query(MonthlyCharge).filter(MonthlyCharge.id == monthly_id).one()
        start_date = int(str(expired_monthly.time_created.year) + str(expired_monthly.time_created.strftime('%m')))

        # create new expired monthly based on old monthly charge
        new_expired_charge = ExpiredCharges(
            description = expired_monthly.description,
            amount = expired_monthly.amount,
            tag_id = expired_monthly.tag_id,
            user_id = session['user_id'],
            expiration_limit = expiration_limit,
            start_date = start_date
        )
        db.add(new_expired_charge)
        db.commit()

        # delete old monthly charge from table. 
        db.delete(expired_monthly)
        db.commit()
    except Exception as e:
        db.rollback()
        return render_template('error-page.html', message="Oops, something happened. Please try again.")
    return redirect(request.referrer)


# Delete Monthly Bill
@bp.route('/delete-monthly-charge', methods=['POST'])
def delete_monthly_charge():
    data = request.form
    db = start_db_session()
    try:
        db.query(MonthlyCharge).filter(MonthlyCharge.id == data['monthly-id']).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        return render_template('error-page.html', message="Oops, something happened. Please try again.")
    return redirect(request.referrer)

# Update Expired Charges
@bp.route('/update-expired-charge', methods=['POST'])
def update_expired_charge():
    data = request.form
    db = start_db_session()

    category_id = data['monthly-category']
    expired_price = data['monthly-price']
    expired_description = data['monthly-name']
    expired_id = data['expired-id']
    start_date = data['start-date']
    end_date = data['end-date']
    # need to change the dates to an integer so we can query easier
    start_date = int(start_date.split('-')[0] + start_date.split('-')[1])
    end_date = int(end_date.split('-')[0] + end_date.split('-')[1])

    try:
        db.query(ExpiredCharges).filter(ExpiredCharges.id == expired_id).update({
            'description': expired_description,
            'amount': expired_price,
            'user_id': session['user_id'],
            'tag_id': category_id,
            'expiration_limit': end_date,
            'start_date': start_date
        })
        db.commit()
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops, something happened. Please try again.")
    return redirect(request.referrer)
    
# Delete Expired Charge
@bp.route('/delete-expired-charge', methods=['POST'])
def delete_expired_charge():
    data = request.form
    db = start_db_session()
    try:
        db.query(ExpiredCharges).filter(ExpiredCharges.id == data['expired-id']).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        return render_template('error-page.html', message="Oops, something happened. Please try again.")
    return redirect(request.referrer)