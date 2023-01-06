from flask import Blueprint, request, jsonify, session, redirect, render_template
from app.models import Product, MonthlyCharge
from app.db import start_db_session

bp = Blueprint('api/expenses', __name__, url_prefix='/api')


# Add an expense
@bp.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.form
    db = start_db_session()
    start_date = data['expense-date']
    expiration_limit = int(str(start_date.split('-')[0]) + str(start_date.split('-')[1]))
    if 'monthly-bill' in data:
        try:
            newMonthly = MonthlyCharge(
                description = data['product-name'].strip(),
                tag_id = data['product-category'],
                user_id = session['user_id'],
                amount = data['product-price'].strip(),
                time_created = data['expense-date'],
                start_date = expiration_limit
            )
            db.add(newMonthly)
            db.commit()
        except AssertionError:
            db.rollback()
            return render_template('error-page.html', message="Missing fields. Please try again")
        except:
            db.rollback()
            return render_template('error-page.html', message="Expense not added.")
        return redirect(request.referrer)
    else:
        try:
            newExpense = Product(
                description = data['product-name'].strip(),
                tag_id = data['product-category'],
                user_id = session['user_id'],
                amount = data['product-price'].strip(),
                time_created = data['expense-date']
            )
            db.add(newExpense)
            db.commit()
        except AssertionError:
            db.rollback()
            return render_template('error-page.html', message="Missing fields. Please try again")
        except:
            db.rollback()
            return render_template('error-page.html', message="Expense not added.")
    return redirect(request.referrer)


# Update Expense
@bp.route('/update-expense', methods=['POST'])
def update_expense():
    data = request.form 
    db = start_db_session()
    start_date = data['expense-date-current']
    if 'monthly-bill' in data:
        try:
            expiration_limit = int(str(start_date.split('-')[0]) + str(start_date.split('-')[1]))
            newMonthly = MonthlyCharge(
                description = data['product-name'].strip(),
                tag_id = data['product-category'],
                user_id = session['user_id'],
                amount = data['product-price'].strip(),
                time_created = data['expense-date-current'],
                start_date = expiration_limit
            )
            db.add(newMonthly)
            db.commit()

            db.query(Product).filter(Product.id == data['product-id']).delete()
            db.commit()
        except AssertionError:
            db.rollback()
            return render_template('error-page.html', message="Missing fields. Please try again")
        except:
            db.rollback()
            return render_template('error-page.html', message="Expense not updated.")
        return redirect(request.referrer)
    else:
        try:
            db.query(Product).filter(Product.id == data['product-id']).update({
                'description': data['product-name'].strip(),
                'tag_id': data['product-category'],
                'user_id': session['user_id'],
                'amount': data['product-price'].strip(),
                'time_created': data['expense-date-current']
            })
            db.commit()
        except AssertionError:
            db.rollback()
            return render_template('error-page.html', message="Missing fields. Please try again")
        except:
            db.rollback()
            return render_template('error-page.html', message="Expense not updated.")
        return redirect(request.referrer)


#Delete Expense
@bp.route('/delete-expense', methods=['POST'])
def delete_expense():
    db = start_db_session()
    data = request.form
    try:
        db.query(Product).filter(Product.id == data['product-id']).delete()
        db.commit()
    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Expense not deleted.")
    return redirect(request.referrer)