from flask import render_template, request,jsonify, session, Blueprint
# import os
# from functools import wraps
# import jwt
# from dotenv import load_dotenv
# from app import app


# load_dotenv


# app.config['SECRET_KEY'] = os.getenv('JWT_SECRET')

# Authentication Decorator
# def token_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         token = request.args.get('token')
#         if not token:
#             return jsonify({'Alert!': 'Token is missing!'}), 403
#         try:
#             payload = jwt.decode(token, key=app.config['SECRET_KEY'], algorithm="HS256")
#         except:
#             return jsonify({'Alert!': 'Invalid Token!'})
#         return func(*args, **kwargs)
#     return decorated


# Create Blueprint
bp = Blueprint('site', __name__)


# Home Route
@bp.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')
    
# practice route
@bp.route('/test')
def test():
    return 'You are in the TEST route'


# For Authenticated
@bp.route('/auth')
def auth():
    return 'You are verified, welcome to dash'
    