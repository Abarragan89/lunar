from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import home, api
from app.db import init_db

load_dotenv()

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

def rgbaToRgb(rgba):
    color_nums = rgba[rgba.find("(")+1:rgba.find(")")].split(',')
    return '#%02x%02x%02x' % (int(color_nums[0]), int(color_nums[1]), int(color_nums[2]))


def create_app():
    # set up app config
    app = Flask(__name__, static_url_path='/')
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SESSION_SECRET')
    )
    
    #register routes
    app.register_blueprint(home)
    app.register_blueprint(api)
    init_db(app)

 
    app.jinja_env.globals.update(rgbaToRgb=rgbaToRgb)
    app.jinja_env.globals.update(format_date_ending=format_date_ending)

    
    return app


