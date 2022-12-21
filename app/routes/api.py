from flask import Blueprint, request, jsonify, session, redirect, render_template
import sqlalchemy
from app.models import User, Tag, Product, Cash
from app.db import start_db_session


bp = Blueprint('api', __name__, url_prefix='/api')

# Login 
@bp.route('/signup', methods=['POST'])
def signup():
    db = start_db_session()
    data = request.form
    try:
        # try making new user
        newUser = User(
            username = data['username'],
            username_lowercase = data['username'].lower(),
            email = data['email'],
            password = data['password'],
            monthly_income = data['monthly-income']
        )
        db.add(newUser)
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 500
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        return jsonify(message='Username or email already taken.'), 500
    except:
        db.rollback()
        return jsonify(message='Sign up failed.'), 500

    # create session
    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True

    return redirect('/')


# Log out
@bp.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

# Log In
@bp.route('/login', methods=['POST'])
def login():
    data = request.form
    db = start_db_session()

    try:
        user = db.query(User).filter(
            User.email == data['email']
        ).one()
    except:
        return jsonify(message='Incorrect credentials'), 400

    if user.verify_password(data['password']) == False:
        return jsonify(message='Incorrect credentials')
    
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return redirect('/')

# Add a Category
@bp.route('/add-category', methods=['POST'])
def add_category():
    data = request.form
    db = start_db_session()

    try:
        newTag = Tag(
            tag_name = data['category-name'],
            tag_color = data['category-color'],
            user_id = session['user_id']
        )
        db.add(newTag)
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Tag not added'), 500
    return redirect('/')

# Add an expense
@bp.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.form
    db = start_db_session()
    monthly_bill = False

    if 'monthly-bill' in data:
        monthly_bill = True

    try:
        newExpense = Product(
            description = data['product-name'],
            tag_id = data['product-category'],
            user_id = session['user_id'],
            amount = data['product-price'],
            monthly_bill = monthly_bill
        )
        db.add(newExpense)
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Expense not added'), 500
    return redirect('/')

# Add Cash
@bp.route('/add-cash', methods=['POST'])
def add_cash():
    data = request.form
    db = start_db_session()
    try:
        newCash = Cash(
            description = data['money-description'],
            amount = data['amount'],
            user_id = session['user_id']
        )
        db.add(newCash)
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Cash not added'), 500
    return redirect('/')

# Update Expense
@bp.route('/update-expense', methods=['POST'])
def update_expense():
    data = request.form 
    db = start_db_session()
    monthly_bill = False
    if 'monthly-bill' in data:
        monthly_bill = True
    try:
        db.query(Product).filter(Product.id == data['product-id']).update({
            'description': data['product-name'],
            'tag_id': data['product-category'],
            'user_id': session['user_id'],
            'amount': data['product-price'],
            'monthly_bill': monthly_bill,
            'time_created': data['expense-date']
        })
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Expense not updated'), 500
    return redirect('/')

#Delete Expense
@bp.route('/delete-expense', methods=['POST'])
def delete_expense():
    db = start_db_session()
    data = request.form
    try:
        db.query(Product).filter(Product.id == data['product-id']).delete()
        db.commit()
    except:
        db.rollback()
        return jsonify(message='Expense not deleted'), 500
    return redirect('/')





# Update Deposit
@bp.route('/edit-deposit', methods=['POST'])
def update_deposit():
    data = request.form 
    db = start_db_session()
    try:
        db.query(Cash).filter(Cash.id == data['cash-id']).update({
            'description': data['money-description'],
            'amount': data['amount'],
            'user_id': session['user_id'],
            'time_created': data['deposit-date']
        })
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Tag not added'), 500
    return redirect('/')

#Delete Expense
@bp.route('/delete-deposit', methods=['POST'])
def delete_deposit():
    db = start_db_session()
    data = request.form
    try:
        db.query(Cash).filter(Cash.id == data['cash-id']).delete()
        db.commit()
    except:
        db.rollback()
        return jsonify(message='Deposit not deleted'), 500
    return redirect('/')