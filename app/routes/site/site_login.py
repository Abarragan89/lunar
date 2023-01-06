from flask import Blueprint, render_template, session, redirect


# Create Blueprint
bp = Blueprint('site_login', __name__)


# link to verify your account
@bp.route('/verify/<query_string>/')
def verify_account(query_string):
    return render_template('verify-account.html')


@bp.route('/')
def home():
    """This route graps all Tags, Expenses joined with Tags, and User data"""
    is_loggedin = session.get('loggedIn')
    if is_loggedin:
        return redirect('/dashboard')
    else:
        return render_template('index.html')


@bp.route('/login')
def login():
    if session.get('loggedIn'):
        return redirect('/dashboard')
    return render_template('login.html')


@bp.route('/signup')
def signup():
    if session.get('loggedIn'):
        return redirect('/dashboard')
    return render_template('signup.html')

@bp.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')


@bp.route('/reset-password/<query_string>')
def reset_password(query_string):
    return render_template('reset-password.html')
