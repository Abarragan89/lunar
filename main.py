from flask import Flask, render_template, request, jsonify, make_response, session
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from functools import wraps

load_dotenv


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET')


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 403
        try:
            payload = jwt.decode(token, key=app.config['SECRET_KEY'], algorithm="HS256")
        except:
            return jsonify({'Alert!': 'Invalid Token!'})
        return func(*args, **kwargs)
    return decorated


# Home Route
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')


# For Public
@app.route('/public')
def public():
    return 'For public'


# For Authenticated
@app.route('/auth')
@token_required
def auth():
    return 'You are verified, welcome to dash'


# Login 
@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == "123456":
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'exp': datetime.utcnow() + timedelta(seconds=120)
        },
        app.config['SECRET_KEY'], algorithm="HS256")
        return token
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: Authentication Failed!'})


if __name__ == '__main__':
    app.run(debug=True)
