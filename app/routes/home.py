from flask import Blueprint, render_template, session

# Create Blueprint
bp = Blueprint('site', __name__)


# Home Route
@bp.route('/')
def home():
    is_loggedin = session.get('loggedIn')
    return render_template('index.html', loggedIn=is_loggedin)

@bp.route('/login')
def login():
    is_loggedin = session.get('loggedIn')
    if is_loggedin == True:
        return render_template('/')
    else:
        return render_template('login.html')