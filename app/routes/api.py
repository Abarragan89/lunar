from flask import Blueprint, request, jsonify, session, redirect, render_template
import sqlalchemy
from app.models import User, Tag, Product, Cash
from app.db import start_db_session

bp = Blueprint('api', __name__, url_prefix='/api')

# Sign up 
@bp.route('/signup', methods=['POST'])
def signup():
    db = start_db_session()
    data = request.form
    try:
        # try making new user
        newUser = User(
            username = data['username'].strip(),
            username_lowercase = data['username'].lower().strip(),
            email = data['email'].strip(),
            password = data['password'].strip(),
            monthly_income = data['monthly-income'].strip()
        )
        db.add(newUser)
        db.commit()
        # give user basic categories
        tag_names = ['Mortgage-Rent', 'Dining', 'Groceries', 'Presents', 'Bills', 'Entertainment', 'Investments', 'Travel', 'Shopping', 'Alcohol']
        tag_colors =['#da3dad', '#6f20e2', '#140eee', '#1a593e', '#00bc69', '#cfe221', '#c47106','#e8b565', '#1bdcc8', '#cf0938']
        for num in range(10):
            newTag = Tag(
                tag_name = tag_names[num],
                tag_color = tag_colors[num],
                user_id = newUser.id
            )
            db.add(newTag)
            db.commit()
    except AssertionError:
        db.rollback()
        print('assertion error')
        return render_template('signup-fail.html', 
            error='Please fill in all fields.',
            username = data['username'].strip(),
            email = data['email'].strip(),
            monthly_income = data['monthly-income'].strip()
            )
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        print('Not unique')
        return render_template('signup-fail.html', 
            error='Email is already taken.',
            username = data['username'].strip(),
            email = data['email'].strip(),
            monthly_income = data['monthly-income'].strip()
            )
    except:
        db.rollback()
        print('other error')
        return render_template('signup-fail.html', 
            error='An error occurred. Please try again',
            username = data['username'].strip(),
            email = data['email'].strip(),
            monthly_income = data['monthly-income'].strip()
            )

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
            User.email == data['email'].strip()
        ).one()
    except:
        return render_template('login-fail.html', error='User not found.', email=data['email'].strip())

    if user.verify_password(data['password']) == False:
        return render_template('login-fail.html', error='Incorrect credentials.', email=data['email'].strip())
    
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return redirect('/')


# Update user data
@bp.route('/update-user-info', methods=['POST'])
def update_user():
    data = request.form
    db = start_db_session()
    try:
        user_data = db.query(User).filter(User.id == session['user_id']).one()
        user_data.monthly_income = data['monthly_income'].strip()
        user_data.username = data['username'].strip()
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='User info not updated'), 500
    return redirect(request.referrer)


# Add a Category
@bp.route('/add-category', methods=['POST'])
def add_category():
    data = request.form
    db = start_db_session()

    try:
        newTag = Tag(
            tag_name = data['category-name'].strip(),
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
    return redirect(request.referrer)

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
            description = data['product-name'].strip(),
            tag_id = data['product-category'],
            user_id = session['user_id'],
            amount = data['product-price'].strip(),
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
    return redirect(request.referrer)

# Add Cash
@bp.route('/add-cash', methods=['POST'])
def add_cash():
    data = request.form
    db = start_db_session()
    try:
        newCash = Cash(
            description = data['money-description'].strip(),
            amount = data['amount'].strip(),
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
    return redirect(request.referrer)

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
            'description': data['product-name'].strip(),
            'tag_id': data['product-category'],
            'user_id': session['user_id'],
            'amount': data['product-price'].strip(),
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
    return redirect(request.referrer)

#Delete Expense
@bp.route('/delete-expense', methods=['POST'])
def delete_expense():
    db = start_db_session()
    data = request.form
    try:
        db.query(Product).filter(Product.id == data['product-id'].strip()).delete()
        db.commit()
    except:
        db.rollback()
        return jsonify(message='Expense not deleted'), 500
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
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Tag not added'), 500
    return redirect(request.referrer)


# Delete Cash deposit
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
    return redirect(request.referrer)


# Update Category
@bp.route('/edit-category', methods=['POST'])
def edit_category():
    data = request.form 
    db = start_db_session()
    print('category id', data['category-id'])
    print('category color', data['category-color'])
    print('category name', data['category-name'])

    try:
        current_tag = db.query(Tag).filter(Tag.id == data['category-id']).one()
        current_tag.tag_color = data['category-color'].strip()
        current_tag.tag_name = data['category-name'].strip()
        db.commit()
    except AssertionError:
        db.rollback()
        return jsonify(message='Missing fields.'), 400
    except:
        db.rollback()
        return jsonify(message='Tag not updated'), 500
    return redirect(f"/categories/{data['category-name']}")


# Delete Category
@bp.route('/delete-category', methods=['POST'])
def delete_category():
    db = start_db_session()
    data = request.form
    try:
        db.query(Tag).filter(Tag.id == data['category-id']).delete()
        db.commit()
    except:
        db.rollback()
        return jsonify(message='Deposit not deleted'), 500
    return redirect('/')