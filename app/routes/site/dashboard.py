from flask import Blueprint, render_template, session, request
from sqlalchemy import extract, desc
from app.models import User, Tag, Product, Cash, MonthlyCharge, ActiveSalary
from app.db import start_db_session
import datetime
from sqlalchemy.sql import func
from ..helper_functions import days_until_first

# Global varialbes that help filter relevant data
days_until_first_data = days_until_first()
today = datetime.datetime.now()

current_month = today.strftime('%m')
current_year = today.year

# Create Blueprint
bp = Blueprint('site_dashboard', __name__)

@bp.route('/dashboard')
def dashboard():
    """This route graps all Tags, Expenses joined with Tags, and User data"""
    is_loggedin = session.get('loggedIn')
    user_id = session.get('user_id')
    user_data = ''
    user_cash = 0
    salaries = 0
    auto_deductions = 0

    db = start_db_session()

    try:

        # Get all tags
        allTags = (
            db.query(Tag)
            .filter(Tag.user_id == user_id)
            .filter(Tag.active == True)
            .all()
        )
        # Get last 7 purchases with joined with tags for activity display; will be mixed with add_cash data
        purchase_data = db.query(Product.time_created, Product.amount, Product.description, Tag.tag_name, Tag.id, Product.id
            ).filter(Product.user_id == user_id
            ).join(Tag
            ).order_by(desc(Product.time_created)
            ).limit(7).all()
        
        # Get last 5 cash addition to display
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
            active_salary = db.query(ActiveSalary).filter(ActiveSalary.user_id == user_id).first()

            # check if user has added extra monthly cash
            user_cash = db.query(func.sum(Cash.amount).label("total_value")
            ).filter(Cash.user_id == user_id
            ).filter(extract('month', Cash.time_created)==current_month
            ).filter(extract('year', Cash.time_created)==current_year
            ).all()
            # set it to zero instead of None if nothing has been added
            user_cash = 0 if user_cash[0][0] is None else round(user_cash[0][0], 2)

        # Get data for the charts
        allMonthlyPurchases = db.query(Tag.tag_name, Tag.tag_color, Product.amount
            ).filter(Product.user_id == user_id
            ).filter(extract('month', Product.time_created)==current_month
            ).filter(extract('year', Product.time_created)==current_year
            ).join(Tag
            ).all()
        
        # This is for monthly charges mixed with purchases. Format has to be idential with the one above(can refactor this)
        monthly_charges_data_wheel = db.query(Tag.tag_name, Tag.tag_color, MonthlyCharge.amount
            ).filter(MonthlyCharge.user_id == session['user_id']
            ).join(Tag
            ).all()
        
        # Change this query to just getting monthly charges to display on 'monthly charges'
        monthly_charges = db.query(MonthlyCharge.time_created, MonthlyCharge.amount, MonthlyCharge.description, Tag.tag_name, Tag.id, MonthlyCharge.id, MonthlyCharge.start_date
            ).filter(MonthlyCharge.user_id == session['user_id']
            ).join(Tag
            ).all()
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
    
    allMonthlyExpenses = allMonthlyPurchases + monthly_charges_data_wheel

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
    # default active salary to zero if there is no active salary
    active_salary = 0 if active_salary is None else active_salary.salary_amount

    
    return render_template (
        'dashboard.html',
        loggedIn=is_loggedin,
        tags=allTags,
        activity_data=activity_data,
        active_salary=active_salary,
        total_monthly_expenses=total_monthly_expenses,
        user_data=user_data,
        salaries=salaries,
        category_data=monthly_charges,
        auto_deductions=auto_deductions,
        days_until_first=days_until_first_data,
        user_cash=user_cash,
        today=today,
        # Chart Data:
        relevant_tag_names=relevant_tag_names,
        values=tag_total,
        relevant_tag_colors=relevant_tag_colors,
    )