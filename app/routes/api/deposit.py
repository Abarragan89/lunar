from flask import Blueprint, request, session, redirect, render_template
from app.models import Cash
from app.db import start_db_session

bp = Blueprint('api/deposits', __name__, url_prefix='/api')


# Add Deposit
@bp.route('/add-cash', methods=['POST'])
def add_cash():
    data = request.form
    db = start_db_session()
    try:
        newCash = Cash(
            description = data['money-description'].strip(),
            amount = data['amount'].strip(),
            user_id = session['user_id'],
            time_created = data['add-cash-date']
        )
        db.add(newCash)
        db.commit()
    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Cash not added.")
    return redirect(request.referrer)


# Update Deposit
@bp.route('/edit-deposit', methods=['POST'])
def update_deposit():
    data = request.form 
    db = start_db_session()
    try:
        db.query(Cash).filter(Cash.id == data['cash-id']).update({
            'description': data['money-description'].strip(),
            'amount': data['amount'].strip(),
            'user_id': session['user_id'],
            'time_created': data['deposit-date']
        })
        db.commit()
    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Cash not added.")
    return redirect(request.referrer)


# Delete Cash deposit
@bp.route('/delete-deposit', methods=['POST'])
def delete_deposit():
    db = start_db_session()
    data = request.form
    try:
        db.query(Cash).filter(Cash.id == data['cash-id']).delete()
        db.commit()
    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Cash not deleted.")
    return redirect(request.referrer)