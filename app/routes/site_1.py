from flask import Blueprint, render_template, session, redirect
from sqlalchemy import extract, desc
from app.models import User, Tag, Product, Cash, Salary, MonthlyCharge
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
    if is_loggedin:
        return redirect('/dashboard')
    else:
        return render_template('index.html')


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/signup')
def signup():
    return render_template('signup.html')

@bp.route('/dashboard')
def dashboard():
    """This route graps all Tags, Expenses joined with Tags, and User data"""
    is_loggedin = session.get('loggedIn')
    user_id = session.get('user_id')
    user_data = ''
    user_cash = 0
    salaries = 0
    db = start_db_session()

    # Get all tags
    allTags = (
        db.query(Tag)
        .filter(Tag.user_id == user_id)
        .all()
    )
    # Get all purchases with joined with tags for activity display will be mixed with deposit data
    purchase_data = db.query(Product.time_created, Product.amount, Product.description, Tag.tag_name, Tag.id, Product.id
        ).filter(Product.user_id == user_id
        ).join(Tag
        ).order_by(desc(Product.time_created)
        ).limit(10).all()
    
    # Get last 20 cash addition to display
    add_cash_data = db.query(Cash.time_created, Cash.amount,  Cash.description, Cash.id
        ).filter(Cash.user_id == user_id
        ).order_by(desc(Cash.time_created)
        ).limit(5).all()

    activity_data = add_cash_data + purchase_data
    activity_data = sorted(activity_data, reverse=True, key = lambda x: x[0])

    # Query to get total in current monthly expenses (minus monthly bills. Those are added separately)
    total_monthly_expenses = db.query(func.sum(Product.amount).label("total_value")
        ).filter(Product.user_id == user_id
        ).filter(extract('month', Product.time_created)==current_month
        ).filter(extract('year', Product.time_created)==current_year
        ).all()
    # Set value to integer zero so calculation won't break
    total_monthly_expenses = 0 if total_monthly_expenses[0][0] is None else round(total_monthly_expenses[0][0], 2)


    # Get Auto Deductions Sum to always subtract. These are the expenses that are monthly bills
    auto_deductions = db.query(func.sum(MonthlyCharge.amount).label("auto_deductions")
        ).filter(MonthlyCharge.user_id == user_id
        ).all()
    
    # Set value to integer zero so calculation won't break
    auto_deductions = 0 if auto_deductions[0][0] is None else round(auto_deductions[0][0], 2)

    # Get User Data if logged in
    if 'user_id' in session:
        user_data = db.query(User).filter(User.id == user_id).one()
        salaries = db.query(Salary).filter(Salary.user_id == user_id).all()

        # check if user has added extra monthly cash
        user_cash = db.query(func.sum(Cash.amount).label("total_value")
        ).filter(Cash.user_id == user_id
        ).filter(extract('month', Cash.time_created)==current_month
        ).filter(extract('year', Cash.time_created)==current_year
        ).all()
        # set it to zero instead of None if nothing has been added
        user_cash = 0 if user_cash[0][0] is None else round(user_cash[0][0], 2)

    # Get data for the charts
    allMonthlyExpenses = db.query(Tag.tag_name, Tag.tag_color, Product.amount
        ).filter(Product.user_id == user_id
        ).filter(extract('month', Product.time_created)==current_month
        ).filter(extract('year', Product.time_created)==current_year
        ).join(Tag
        ).all()
    
    # Create a chartData object to remove repeated Tags in products, and add up the total in products
    chartData = {}
    for expense in allMonthlyExpenses:
        if expense[0] in chartData:
            chartData[expense[0]]['product_amount'] += expense[2]
        else:
            chartData[expense[0]] = {'tag_color': expense[1], 'product_amount': expense[2]} 
    
    # Getting data from dictionary to get three distinct lists with relevant data to pass
    values = chartData.values()
    relevant_tag_names = [ tag_name for tag_name in chartData.keys()]
    tag_total = [float(item['product_amount']) for item in values]
    relevant_tag_colors = [item['tag_color'] for item in values]

    # Change this query to just getting monthly charges
    user_category = db.query(MonthlyCharge.time_created, MonthlyCharge.amount, MonthlyCharge.description, Tag.tag_name, Tag.id, MonthlyCharge.id
        ).filter(MonthlyCharge.user_id == session['user_id']
        ).join(Tag
        ).all()
    
    return render_template (
        'dashboard.html',
        loggedIn=is_loggedin,
        tags=allTags,
        activity_data=activity_data,
        total_monthly_expenses=total_monthly_expenses,
        user_data=user_data,
        salaries=salaries,
        category_data=user_category,
        auto_deductions=auto_deductions,
        days_until_first=days_until_first_data,
        user_cash=user_cash,
        today=today,
        # Chart Data:
        relevant_tag_names=relevant_tag_names,
        values=tag_total,
        relevant_tag_colors=relevant_tag_colors
    )
    


@bp.route('/profile')
def profile():
    db = start_db_session()
    user_id = session.get('user_id')
    is_loggedin = session.get('loggedIn')
    user_data = db.query(User).filter(User.id == session['user_id']).one()
    salaries = db.query(Salary).filter(Salary.user_id == user_id).order_by(desc(Salary.time_created)).all()

    
    allTags = (
        db.query(Tag)
        .filter(Tag.user_id == user_id)
        .all()
    )
    
    return render_template('profile.html',
        user_data=user_data, 
        salaries=salaries,
        loggedIn=is_loggedin,
        tags = allTags, 
        today=today
    )

# Load the Category Page and Data
@bp.route('/categories/<categoryName>')
def categories(categoryName):
    is_loggedin = session.get('loggedIn')
    user_id = session['user_id']
    db = start_db_session()

    category = (
        db.query(Tag)
        .filter(Tag.user_id == user_id)
        .filter(Tag.tag_name == categoryName)
        .one()
    )

    totalAmountSpend= db.query(func.sum(Product.amount).label("total_value")
        ).filter(Product.user_id == user_id
        ).filter(Product.tag_id == category.id).all()
    totalAmountSpend = totalAmountSpend[0][0]

    purchase_data = db.query(Product.time_created, Product.amount, Product.description, Tag.tag_name, Tag.id, Product.id
        ).filter(Product.user_id == user_id
        ).filter(Product.tag_id == category.id
        ).join(Tag
        ).order_by(desc(Product.time_created)
        ).all()
    
    allTags = (
        db.query(Tag)
        .filter(Tag.user_id == user_id)
        .all()
    )

    return render_template('categories.html',
        loggedIn=is_loggedin,
        category=category,
        total=totalAmountSpend,
        allExpenses=purchase_data,
        tags=allTags
    )

@bp.route('/history/<yearMonth>')
def history(yearMonth):
    yearLookUp = yearMonth.split('-')[0]
    monthLookUp = yearMonth.split('-')[1]
    is_loggedin = session.get('loggedIn')
    user_id = session['user_id']
    
    db = start_db_session()
    # need to get tags for the navbar
    allTags = (
        db.query(Tag)
        .filter(Tag.user_id == user_id)
        .all()
    )
    try:
        salary = db.query(Salary
            ).filter(Salary.user_id == user_id
            ).filter(extract('month', Salary.time_created) == monthLookUp
            ).filter(extract('year', Salary.time_created) == yearLookUp
            ).one()
    except:
        salary = None
    return render_template('history.html',
        loggedIn=is_loggedin,
        tags=allTags,
        salary=salary,
        yearLookUp=yearLookUp,
        monthLookUp=monthLookUp,
        current_month=current_month,
        current_year=current_year
    )