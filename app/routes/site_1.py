from flask import Blueprint, render_template, session
from sqlalchemy import select
from app.models import User, Tag, Product
from app.db import start_db_session

# Create Blueprint
bp = Blueprint('site', __name__)


@bp.route('/')
def home():
    is_loggedin = session.get('loggedIn')
    user_id = session.get('user_id')
    db = start_db_session()
    # Get all tags
    allTags = (
        db.query(Tag)
        .filter(Tag.user_id == user_id)
        .all()
    )
    expenses = db.query(Product, Tag).filter(Product.user_id == user_id).filter(Product.tag_id == Tag.id).all()

    for expense in expenses:
        print(expense[0].product_name, expense[0].price, expense[1].tag_name)

    return render_template('index.html', loggedIn=is_loggedin, tags=allTags, expenses=expenses)

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/signup')
def signup():
    return render_template('signup.html')


@bp.route('/add_expense')
def add_expense():
    return render_template('add_expense_modal.html')

