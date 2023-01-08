from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import login, categories, expense, deposit, profile, charges
from app.routes import site_login, dashboard, site_profile, site_categories, site_history, error_page
from app.db import init_db
from flask_mail import Mail
from datetime import date


load_dotenv()

# Helper functions
def format_date_ending(date):
    date_num = int(date)
    last_digit = date_num % 10
    if last_digit == 1 and date_num != 11:
        return 'st'
    elif last_digit == 2 and date_num != 12:
        return 'nd'
    elif last_digit == 3 and date_num != 13:
        return 'rd'
    else:
        return 'th'

def rgbToHex(rgb):
    color_nums = rgb[rgb.find("(")+1:rgb.find(")")].split(',')
    return '#%02x%02x%02x' % (int(color_nums[0]), int(color_nums[1]), int(color_nums[2]))

def convertExpirationDate(int):
    string_int = str(int)
    return f"{string_int[4:]}/{string_int[:4]}"

def format_date(integer, option):
    yearMonthString = str(integer)
    salaryYear = int(yearMonthString[:4])
    salaryMonth = int(yearMonthString[4:])

    newDateTimeObj = date(year=salaryYear, month=salaryMonth, day=1)

    if (option == 'monthName/year'):
        return f'{newDateTimeObj.strftime("%b")}/{newDateTimeObj.strftime("%Y")}'



# Creating App
def create_app():
    # set up app config
    app = Flask(__name__, static_url_path='/')
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SESSION_SECRET')
    )

    # Mail configurations
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.getenv('GOOGLE_USER')
    app.config['MAIL_PASSWORD'] = os.getenv('GOOGLE_PASSWORD')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.mail = Mail(app)

    #register routes
    app.register_blueprint(login)
    app.register_blueprint(categories)
    app.register_blueprint(expense)
    app.register_blueprint(deposit)
    app.register_blueprint(profile)
    app.register_blueprint(charges)
    app.register_blueprint(site_login)
    app.register_blueprint(dashboard)
    app.register_blueprint(site_profile)
    app.register_blueprint(site_categories)
    app.register_blueprint(site_history)
    app.register_blueprint(error_page)

    init_db(app)

    # helper functions
    app.jinja_env.globals.update(rgbToHex=rgbToHex)
    app.jinja_env.globals.update(format_date_ending=format_date_ending)
    app.jinja_env.globals.update(convertExpirationDate=convertExpirationDate)
    app.jinja_env.globals.update(format_date=format_date)
    
    return app
