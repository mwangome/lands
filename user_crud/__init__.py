# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from urllib.parse import quote_plus
from flask_qrcode import QRcode

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    application = Flask(__name__)

    application.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + quote_plus('Admin123#@!') + '@localhost:3306/lands'
    QRcode(application)
    db.init_app(application)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(application)

    from .models import TblUser

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return TblUser.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    application.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)

    return application