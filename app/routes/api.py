from flask import Blueprint, request, jsonify, session, redirect, render_template
import sqlalchemy
from app.models import User
from app.db import start_db_session
import sys

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
        print(sys.exc_info()[0])
        db.rollback()
        return jsonify(message='Missing fields.'), 500
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        print(sys.exc_info()[0])
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
        print(sys.exc_info()[0])
        return jsonify(message='Incorrect credentials'), 400

    if user.verify_password(data['password']) == False:
        return jsonify(message='Incorrect credentials')
    
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return redirect('/')