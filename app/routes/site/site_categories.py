from flask import Blueprint, render_template, session
from sqlalchemy import desc
from app.models import  Tag, Product
from app.db import start_db_session
from sqlalchemy.sql import func

# Create Blueprint
bp = Blueprint('site_categories', __name__)


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
        .filter(Tag.active == True)
        .all()
    )
    
    return render_template('categories.html',
        loggedIn=is_loggedin,
        category=category,
        total=totalAmountSpend,
        allExpenses=purchase_data,
        tags=allTags
    )