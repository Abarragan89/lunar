from flask import Blueprint, request, session, redirect, render_template, current_app
import datetime
from app.models import User, Tag, TempUser, ConfirmationToken
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
        # if user exists, then send them to error page to try again
        user_exists = db.query(User).filter(User.email == data['email'].strip()).first()
        if user_exists:
            db.rollback()
            return render_template('signup-fail.html', 
                error='Email is already taken.',
                username = data['username'].strip(),
                email = data['email'].strip(),
                )
    except AssertionError:
        db.rollback()
        print('assertion error')
        return render_template('signup-fail.html', 
            error='Please fill in all fields.',
            username = data['username'].strip(),
            email = data['email'].strip(),
            )
    except Exception as e:
        print(e)
        db.rollback()
        return render_template('signup-fail.html', 
            error='An error occurred. Please try again',
            username = data['username'].strip(),
            email = data['email'].strip(),
            )
    # this only runs if the above code does not run and there is no user with that email.
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
        )
        db.add(newUser)
        db.commit()
        if newUser:
            msg = Message('Lunaris: Verify Your Account', sender = 'anthony.bar.89@gmail.com', recipients = [newUser.email])
            verificationLink = f"{request.base_url.split('/')[0] + request.base_url.split('/')[1]}//{request.base_url.split('/')[2]}/verify/{result}"
            # msg.body = f"Just one more step,\nUse the link below to verify your account and take ownership of your finances!\n\n  {request.base_url.split('/')[0] + request.base_url.split('/')[1]}//{request.base_url.split('/')[2]}/verify/{result}\n -Lunaris"
            msg.html = f"<p>Just one more step,</p>\n<p>Use the link below to verify your account and take ownership of your finances!</p>\n\n <a href='{verificationLink}'> Click Here </a>\n -Lunaris"
            current_app.mail.send(msg)
    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="User not created. Please try again.")
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
        session.permanent = True

        #delete temp user
        db.delete(temp_user)
        db.commit()

        # Add default tags and colors
        tag_colors =[
                'rgb(160, 30, 30)', 
                'rgb(160, 88, 30)',
                'rgb(160, 153, 30)', 
                'rgb(30, 160, 32)', #green
                'rgb(30, 114, 160)',  
                'rgb(30, 34, 160)',
                'rgb(75, 30, 160)',
                'rgb(125, 30, 160)',
                'rgb(160, 30, 134)',
                'rgb(125, 54, 18)',
                'rgb(153, 187, 27)'
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
                'Automotive', 
                'Subscriptions'
                ]
        for num in range(11):
            newTag = Tag(
                tag_name = tag_names[num],
                tag_color = tag_colors[num],
                user_id = newUser.id
            )
            db.add(newTag)
            db.commit()
    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Account not created. Please try again.")
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
    session.permanent = True

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
            new_token = ConfirmationToken(
                unique_string = result,
                email = user_email
            )
            db.add(new_token)
            db.commit()

            msg = Message('Lunaris: Verify Your Account', sender = 'anthony.bar.89@gmail.com', recipients = [user_email])
            # wanted to get rid of the 'api/forgot-password' in the request url
            msg.body = f"Looks like you forgot something,\nClick the link below to reset your password.\n{request.base_url.split('/')[0] + request.base_url.split('/')[1]}//{request.base_url.split('/')[2]}/reset-password/{new_token.unique_string}\n -Lunaris"
            current_app.mail.send(msg)
    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
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
    except AssertionError:
        db.rollback()
        return render_template('error-page.html', message="Missing fields. Please try again")
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    return render_template('login.html')


@bp.route('/delete-user', methods=['POST'])
def delete_user():
    db = start_db_session()
    user_id = session['user_id']
    try:
        db.query(User).filter(User.id == user_id).delete()
        db.commit()
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    session.clear()
    return redirect('/')




    

