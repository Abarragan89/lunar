from flask import Blueprint, render_template, session, redirect
from sqlalchemy import extract, desc
from app.models import Tag, Product, Cash, Salary, MonthlyCharge, ExpiredCharges, ActiveSalary
from app.db import start_db_session
import datetime
from sqlalchemy.sql import func

# Global varialbes that help filter relevant data
today = datetime.datetime.now()
current_month = today.strftime('%m')
current_year = today.year

# Create Blueprint
bp = Blueprint('site_history', __name__)


@bp.route('/history/<yearMonth>')
def history(yearMonth):
    yearLookUp = yearMonth.split('-')[0]
    monthLookUp = yearMonth.split('-')[1]
    is_loggedin = session.get('loggedIn')
    user_id = session['user_id']

    # combine the year and month to create an integer to compare to expiration limit
    date_limit_int = int(str(yearLookUp) + str(monthLookUp))
    db = start_db_session()
    # need to get tags for the navbar
    allTags = (
        db.query(Tag)
        .filter(Tag.user_id == user_id)
        .filter(Tag.active == True)
        .all()
    )
    try: 
        salary = db.query(func.sum(Salary.salary_amount).label("total_salary_value")
            ).filter(Salary.user_id == user_id
            ).filter(Salary.start_date <= date_limit_int
            ).filter(Salary.last_payment >= date_limit_int
            ).first()
        
        include_active = db.query(ActiveSalary
            ).filter(ActiveSalary.user_id == user_id
            ).filter(ActiveSalary.start_date <= date_limit_int
            ).first()
        
        # get all summed up values of monthly charges and purchases for the month     
        all_purchases_total = db.query(func.sum(Product.amount).label("total_value")
            ).filter(Product.user_id == user_id
            ).filter(extract('month', Product.time_created) == monthLookUp
            ).filter(extract('year', Product.time_created) == yearLookUp
            ).all()
        all_cash_total = db.query(func.sum(Cash.amount).label("total_value")
            ).filter(Cash.user_id == user_id
            ).filter(extract('month', Cash.time_created) == monthLookUp
            ).filter(extract('year', Cash.time_created) == yearLookUp
            ).all()
        past_expired_charges_total = db.query(func.sum(ExpiredCharges.amount).label("total_value")
            ).filter(ExpiredCharges.user_id == user_id
            ).filter(ExpiredCharges.expiration_limit >= date_limit_int
            ).filter(ExpiredCharges.start_date <= date_limit_int
            ).all()
        any_current_monthly_total = db.query(func.sum(MonthlyCharge.amount).label("total_value")
            ).filter(MonthlyCharge.user_id == user_id
            ).filter(MonthlyCharge.start_date <= date_limit_int).filter()
        
        expired_charges = db.query(ExpiredCharges.time_created, ExpiredCharges.amount, 
            ExpiredCharges.description, Tag.tag_name, Tag.id, ExpiredCharges.id, ExpiredCharges.start_date, ExpiredCharges.expiration_limit, ExpiredCharges.start_date
        ).filter(ExpiredCharges.user_id == session['user_id']
        ).filter(ExpiredCharges.expiration_limit >= date_limit_int
        ).filter(ExpiredCharges.start_date <= date_limit_int
        ).join(Tag
        ).all()

        active_monthly_charges = db.query(MonthlyCharge.time_created, MonthlyCharge.amount, 
            MonthlyCharge.description, Tag.tag_name, Tag.id, MonthlyCharge.id, MonthlyCharge.start_date
        ).filter(MonthlyCharge.user_id == session['user_id']
        ).filter(MonthlyCharge.start_date <= date_limit_int
        ).join(Tag
        ).all()

        all_purchases = db.query(Product.time_created, Product.amount, Product.description, Tag.tag_name, Tag.id, Product.id
            ).filter(Product.user_id == user_id
            ).filter(extract('month', Product.time_created) == monthLookUp
            ).filter(extract('year', Product.time_created) == yearLookUp
            ).join(Tag
            ).all()
        
        added_cash_data = db.query(Cash.time_created, Cash.amount,  Cash.description, Cash.id
        ).filter(Cash.user_id == user_id
        ).filter(extract('month', Cash.time_created) == monthLookUp
        ).filter(extract('year', Cash.time_created) == yearLookUp
        ).order_by(desc(Cash.time_created)
        ).all()

    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")

    # set defaults to query objects in case they come up empty
    salary = 0 if salary.total_salary_value is None else salary.total_salary_value
    if include_active:
        salary = salary + include_active.salary_amount    

    all_cash_total = 0 if all_cash_total[0].total_value is None else all_cash_total[0].total_value
    past_expired_charges_total = 0 if past_expired_charges_total[0].total_value is None else past_expired_charges_total[0].total_value
    any_current_monthly_total = 0 if any_current_monthly_total[0].total_value is None else any_current_monthly_total[0].total_value
    all_purchases_total = 0 if all_purchases_total[0].total_value is None else all_purchases_total[0].total_value
    # Add up expired and any current monthly to get total monthly expenses
    total_monthly_expenses = past_expired_charges_total + any_current_monthly_total

    try:
         # Get data for the charts
        allMonthlyPurchases = db.query(Tag.tag_name, Tag.tag_color, Product.amount
            ).filter(Product.user_id == user_id
            ).filter(extract('month', Product.time_created)==monthLookUp
            ).filter(extract('year', Product.time_created)==yearLookUp
            ).join(Tag
            ).all()
        
        # This is for monthly charges mixed with purchases. Format has to be idential with the one above(can refactor this)
        monthly_charges_data_wheel = db.query(Tag.tag_name, Tag.tag_color, MonthlyCharge.amount
            ).filter(MonthlyCharge.user_id == session['user_id']
            ).filter(extract('month', Product.time_created)==monthLookUp
            ).filter(extract('year', Product.time_created)==yearLookUp
            ).join(Tag
            ).all()
    
        
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
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")
        

    return render_template('history.html',
        loggedIn=is_loggedin,
        tags=allTags,
        salary=salary,
        yearLookUp=yearLookUp,
        monthLookUp=monthLookUp,
        current_month=current_month,
        current_year=current_year,
        total_monthly_expenses=total_monthly_expenses,
        all_purchases_total=all_purchases_total,
        all_purchases=all_purchases,
        expired_charges=expired_charges,
        active_monthly_charges=active_monthly_charges,
        all_cash_total=all_cash_total,
        added_cash_data=added_cash_data,
        # Chart Data:
        relevant_tag_names=relevant_tag_names,
        values=tag_total,
        relevant_tag_colors=relevant_tag_colors
    )




#redirection for user clearing out the calendar in history
@bp.route('/history')
def redirect_for_clear_history():
    return redirect(f'/history/{current_year}-{current_month}')