from flask import render_template, request,jsonify, session, make_response, Blueprint
from datetime import datetime, timedelta 
import os
from functools import wraps
import jwt
from dotenv import load_dotenv


load_dotenv

# app.config['SECRET_KEY'] = os.getenv('JWT_SECRET')

bp = Blueprint('/api', __name__, url_prefix='/api')


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


# Login 
@bp.route('/login', methods=['POST'])
def login():











    # if request.form['username'] and request.form['password'] == "123456":
    #     session['logged_in'] = True
    #     token = jwt.encode({
    #         'user': request.form['username'],
    #         'exp': datetime.utcnow() + timedelta(seconds=120)
    #     },
    #     bp.config['SECRET_KEY'], algorithm="HS256")
    #     return token
    # else:
    #     return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: Authentication Failed!'})