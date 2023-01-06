from flask import Blueprint, render_template, session
from sqlalchemy import desc
from app.models import  Tag, Product
from app.db import start_db_session
from sqlalchemy.sql import func

# Create Blueprint
bp = Blueprint('site_error', __name__)

# 404 Page
@bp.route('/error')
def error_page():
    return render_template('error-page.html', message="hello there")