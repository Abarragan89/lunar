from flask import Blueprint, render_template, session
from sqlalchemy import extract
from app.models import User, Tag, Product
from app.db import start_db_session
import datetime
from sqlalchemy.sql import func

today = datetime.datetime.now()
current_month = today.month
current_year = today.year

# Create Blueprint
bp = Blueprint('site', __name__)


@bp.route('/')
def home():
    """This route graps all Tags, Expenses joined with Tags, and User data"""
    is_loggedin = session.get('loggedIn')
    user_id = session.get('user_id')
    user_data = ''
    db = start_db_session()
    
    # Get all tags
    allTags = (
        db.query(Tag)
        .filter(Tag.user_id == user_id)
        .all()
    )
    # Get all expenses
    purchase_data = db.query(Product, Tag
        ).filter(Product.user_id == user_id
        ).filter(Product.tag_id == Tag.id
        ).order_by(Product.time_created
        ).all()


    # Query to get total in current monthly expenses 
    total_monthly_expenses = db.query(func.sum(Product.price).label("total_score")
        ).filter( Product.user_id == user_id
        ).filter(extract('month', Product.time_created)==current_month
        ).filter(extract('year', Product.time_created)==current_year
        ).all()
    total_monthly_expenses = total_monthly_expenses[0]


    # Get Auto Deductions to always subtract
    auto_deductions = db.query(func.sum(Product.price).label("auto_deductions")
        ).filter(Product.user_id == user_id
        ).filter(Product.monthly_bill == True
        ).all()
    auto_deductions = auto_deductions[0]


    # Get User Data if logged in
    if 'user_id' in session:
        user_data = db.query(User).filter(User.id == user_id).one()

    return render_template(
        'index.html',
        loggedIn=is_loggedin,
        tags=allTags,
        purchase_data=purchase_data,
        total_monthly_expenses=total_monthly_expenses,
        user_data=user_data,
        auto_deductions=auto_deductions
    )


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/signup')
def signup():
    return render_template('signup.html')


@bp.route('/add_expense')
def add_expense():
    return render_template('add_expense_modal.html')
