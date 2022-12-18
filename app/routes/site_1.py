from flask import Blueprint, render_template, session
# from flask_modals import render_template_modal, Modal

# Create Blueprint
bp = Blueprint('site', __name__)


@bp.route('/')
def home():
    is_loggedin = session.get('loggedIn')
    return render_template('index.html', loggedIn=is_loggedin)

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/signup')
def signup():
    return render_template('signup.html')


@bp.route('/add_expense')
def add_expense():
    return render_template('add_expense_modal.html')

