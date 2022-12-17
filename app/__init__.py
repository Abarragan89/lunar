# from flask import Flask, Blueprint

# from app.routes import site_routes

# app = Flask(__name__)

# from app import models


# if __name__ == "__main__":
#     app.run(debug=True)



# -------------- BOOTCAMP ------------- #

from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import home, dashboard

load_dotenv()


def create_app(test_config=None):
    # set up app config
    app = Flask(__name__, static_url_path='/')
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY=os.getenv('JWT_SECRET')
    )
    
    #register routes
    app.register_blueprint(home)
    app.register_blueprint(dashboard)
    return app


