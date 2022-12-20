from flask import Blueprint, render_template, session
from sqlalchemy import extract, desc
from app.models import User, Tag, Product, Cash
from app.db import start_db_session
import datetime
from sqlalchemy.sql import func
from .helper_functions import days_until_first

# Global varialbes that help filter relevant data
days_until_first_data = days_until_first()
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
    user_cash = 0
    db = start_db_session()

    # Get all tags
    allTags = (
        db.query(Tag)
        .filter(Tag.user_id == user_id)
        .all()
    )

    purchase_data = db.query(Product.time_created, Product.amount, Product.description, Tag.tag_name, Tag.id
        ).filter(Product.user_id == user_id
        ).join(Tag
        ).order_by(desc(Product.time_created)
        ).limit(20).all()
    # # Get last 20 cash addition to display
    add_cash_data = db.query(Cash.time_created, Cash.amount,  Cash.description
        ).filter(Cash.user_id == user_id
        ).order_by(desc(Cash.time_created)
        ).limit(20).all()

    # print('purchase data===========', purchase_data)

    activity_data = add_cash_data + purchase_data
    activity_data = sorted(activity_data, reverse=True, key = lambda x: x[0])

    print('activity data ============', activity_data)

    # Query to get total in current monthly expenses 
    total_monthly_expenses = db.query(func.sum(Product.amount).label("total_value")
        ).filter(Product.user_id == user_id
        ).filter(extract('month', Product.time_created)==current_month
        ).filter(extract('year', Product.time_created)==current_year
        ).all()
    # Set value to integer zero so calculation won't break
    total_monthly_expenses = 0 if total_monthly_expenses[0][0] is None else round(total_monthly_expenses[0][0], 2)


    # Get Auto Deductions to always subtract
    auto_deductions = db.query(func.sum(Product.amount).label("auto_deductions")
        ).filter(Product.user_id == user_id
        ).filter(Product.monthly_bill == True
        ).all()
    # Set value to integer zero so calculation won't break
    auto_deductions = 0 if auto_deductions[0][0] is None else round(auto_deductions[0][0], 2)

    # Get User Data if logged in
    if 'user_id' in session:
        user_data = db.query(User).filter(User.id == user_id).one()

        # check if user has added extra monthly cash
        user_cash = db.query(func.sum(Cash.amount).label("total_value")
        ).filter(Cash.user_id == user_id
        ).all()
        # set it to zero instead of None if nothing has been added
        user_cash = 0 if user_cash[0][0] is None else round(user_cash[0][0], 2)

    return render_template(
        'index.html',
        loggedIn=is_loggedin,
        tags=allTags,

        activity_data=activity_data,

        purchase_data=purchase_data,
        total_monthly_expenses=total_monthly_expenses,
        user_data=user_data,
        auto_deductions=auto_deductions,
        days_until_first=days_until_first_data,
        user_cash=user_cash
        
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

@bp.route('/edit-activity')
def edit_activity():
    return 'hello'
