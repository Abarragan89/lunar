from flask import Blueprint, request, session, redirect, render_template, current_app
import datetime
from app.models import User, Tag, ActiveSalary, TempUser, ConfirmationToken
from app.db import start_db_session
from flask_mail import Message
import uuid

bp = Blueprint('api/login', __name__, url_prefix='/api')

today = datetime.datetime.now()
current_month = today.strftime('%m')
current_year = today.year

# Sign up
@bp.route('/signup', methods=['POST'])
def signup():
    db = start_db_session()
    data = request.form
    try:
        # Make new user
        user_exists = db.query(User).filter(User.email == data['email'].strip()).first()

        if user_exists:
            db.rollback()
            return render_template('signup-fail.html', 
                error='Email is already taken.',
                username = data['username'].strip(),
                email = data['email'].strip(),
                monthly_income = data['monthly-income'].strip()
                )
    except AssertionError:
        db.rollback()
        print('assertion error')
        return render_template('signup-fail.html', 
            error='Please fill in all fields.',
            username = data['username'].strip(),
            email = data['email'].strip(),
            monthly_income = data['monthly-income'].strip()
            )
    except Exception as e:
        print(e)
        db.rollback()
        return render_template('signup-fail.html', 
            error='An error occurred. Please try again',
            username = data['username'].strip(),
            email = data['email'].strip(),
            monthly_income = data['monthly-income'].strip()
            )
    try: 
        # make unique string
        result = uuid.uuid4()
        result = str(result.hex)
        # Make new user
        newUser = TempUser(
            username = data['username'].strip(),
            username_lowercase = data['username'].lower().strip(),
            email = data['email'].strip(),
            unique_id = result,
            salary_amount = data['monthly-income']
        )
        db.add(newUser)
        db.commit()
        if newUser:
            msg = Message('Lunar: Verify Your Account', sender = 'anthony.bar.89@gmail.com', recipients = [newUser.email])
            msg.body = f"Just one more step,\nClick the link below to verify your account and take ownership of your finances!\nLink will expire in 2 minutes.\n{request.base_url.split('/')[0] + request.base_url.split('/')[1] + request.base_url.split('/')[2]}/verify/{result}\n -Lunar"
            current_app.mail.send(msg)
    except Exception as e:
        print('=====================', e)
    return render_template('signup_check_email.html')


# Sign up Verified
@bp.route('/signup_verified', methods=['POST'])
def signup_verified():
    db = start_db_session()
    data = request.form
    temp_user_id = data['temp-user-unique-id']
    user_password = data['user-password']

    try:
        # find temporary user
        temp_user = db.query(TempUser).filter(TempUser.unique_id == temp_user_id).one()

        # Make new user from temp user
        newUser = User(
            username = temp_user.username,
            username_lowercase = temp_user.username_lowercase,
            email = temp_user.email,
            password = user_password
        )
        db.add(newUser)
        db.commit()
        # create session
        session.clear()
        session['user_id'] = newUser.id
        session['loggedIn'] = True

        # Add Salary Model
        newSalary = ActiveSalary (
            salary_amount = temp_user.salary_amount,
            start_date = str(current_year) + str(current_month).rjust(2, '0'),
            user_id = newUser.id
        )
        db.add(newSalary)
        #delete temp user
        db.commit()
        db.delete(temp_user)
        db.commit()

        # Add default tags and colors
        tag_colors =[
                'rgb(255, 0, 0)', 
                'rgb(255, 140, 0)',
                'rgb(212, 255, 0)', 
                'rgb(26, 255, 0)', 
                'rgb(0, 255, 162)',  
                'rgb(0, 191, 255)',
                'rgb(0, 68, 255)',
                'rgb(38, 0, 255)',
                'rgb(153, 0, 255)',
                'rgb(255, 0, 234)',
                'rgb(255, 0, 64)'
                ]
        # give user basic categories
        tag_names = [
                'Mortgage-Rent', 
                'Dining', 
                'Groceries', 
                'Presents', 
                'Bills', 
                'Entertainment', 
                'Investments', 
                'Travel', 
                'Shopping', 
                'Alcohol', 
                'Misc.'
                ]
        for num in range(11):
            newTag = Tag(
                tag_name = tag_names[num],
                tag_color = tag_colors[num],
                user_id = newUser.id
            )
            db.add(newTag)
            db.commit()

    except Exception as e:
        print('============== making new user', e)

    return redirect('/dashboard')


# Log out
@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

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

    return redirect('/dashboard')

# Forgot password
@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.form
    user_email = data['email']
    db =start_db_session()

    result = uuid.uuid4()
    result = str(result.hex)
    user_exists = False
    try:
        user = db.query(User).filter(User.email == user_email).first()
        if user:
            user_exists=True
            try: 
                new_token = ConfirmationToken(
                    unique_string = result,
                    email = user_email
                )
                db.add(new_token)
                db.commit()

                msg = Message('Lunar: Verify Your Account', sender = 'anthony.bar.89@gmail.com', recipients = [user_email])
                # wanted to get rid of the 'api/forgot-password' in the request url
                msg.body = f"Looks like you forgot something,\nClick the link below to reset your password.\n{request.base_url.split('/')[0] + request.base_url.split('/')[1] + request.base_url.split('/')[2]}/reset-password/{new_token.unique_string}\n -Lunar"
                current_app.mail.send(msg)

                return render_template('forgot_password_message.html', user_exists=user_exists)
            except Exception as e:
                print('=============================== maing token',e)
    except Exception as e:
        print(e)
    return render_template('forgot_password_message.html', user_exists=user_exists)

# Reset Password
@bp.route('/reset-password', methods=['POST'])
def reset_password_change():
    data = request.form
    db =start_db_session()

    valid_token = data['validation-token']
    print('validation-token', valid_token)
    try:
        find_token = db.query(ConfirmationToken).filter(ConfirmationToken.unique_string == valid_token).first()
        if find_token:
            find_user = db.query(User).filter(User.email == find_token.email).one()
            find_user.password = data['new-password-confirm']
            db.commit()        
    except Exception as e:
        print('========================',e)
        return render_template('reset-password.html', success=False)
    
    return render_template('login.html')