from flask import Blueprint, render_template, session
from sqlalchemy import desc
from app.models import  Tag, Product, MonthlyCharge, ExpiredCharges
from app.db import start_db_session
from sqlalchemy.sql import func
import datetime

# Create Blueprint
bp = Blueprint('site_categories', __name__)

today = datetime.datetime.now()

current_month = today.strftime('%m')
current_year = today.year

# Load the Category Page and Data
@bp.route('/categories/<categoryName>')
def categories(categoryName):
    is_loggedin = session.get('loggedIn')
    user_id = session['user_id']
    db = start_db_session()
    try:
        category = (
            db.query(Tag)
            .filter(Tag.user_id == user_id)
            .filter(Tag.tag_name == categoryName)
            .one()
        )
        totalPurchaseAmount= db.query(func.sum(Product.amount).label("total_value")
            ).filter(Product.user_id == user_id
            ).filter(Product.tag_id == category.id).all()
        totalPurchaseAmount= totalPurchaseAmount[0][0]
        totalPurchaseAmount = 0 if totalPurchaseAmount is None else totalPurchaseAmount

        totalMonthlyAmount = db.query(func.sum(MonthlyCharge.amount).label("total_value")
            ).filter(MonthlyCharge.user_id == user_id
            ).filter(MonthlyCharge.tag_id == category.id).all()
        totalMonthlyAmount = totalMonthlyAmount[0][0]
        totalMonthlyAmount = 0 if totalMonthlyAmount is None else totalMonthlyAmount


        totalAmountSpent = totalMonthlyAmount + totalPurchaseAmount

        purchase_data = db.query(Product.time_created, Product.amount, Product.description, Tag.tag_name, Tag.id, Product.id
            ).filter(Product.user_id == user_id
            ).filter(Product.tag_id == category.id
            ).join(Tag
            ).order_by(desc(Product.time_created)
            ).all()
        
        monthly_charge_data = db.query(MonthlyCharge.time_created, MonthlyCharge.amount, MonthlyCharge.description, Tag.tag_name, Tag.id, MonthlyCharge.id, MonthlyCharge.start_date
            ).filter(MonthlyCharge.user_id == user_id
            ).filter(MonthlyCharge.tag_id == category.id
            ).join(Tag
            ).order_by(desc(MonthlyCharge.start_date)
            ).all()
        
        allTags = (
            db.query(Tag)
            .filter(Tag.user_id == user_id)
            .filter(Tag.active == True)
            .all()
        )
    except:
        db.rollback()
        return render_template('error-page.html', message="Oops. Something happened. Please try again.")

    
    return render_template('categories.html',
        loggedIn=is_loggedin,
        category=category,
        total=totalAmountSpent,
        allExpenses=purchase_data,
        tags=allTags,
        monthly_charge_data=monthly_charge_data
    )