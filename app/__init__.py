from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import home, dashboard, api
from app.db import init_db

load_dotenv()

def create_app():
    # set up app config
    app = Flask(__name__, static_url_path='/')
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SESSION_SECRET')
    )
    
    #register routes
    app.register_blueprint(home)
    app.register_blueprint(dashboard)
    app.register_blueprint(api)
    init_db(app)

    # modal.init_app(app)
    
    return app


