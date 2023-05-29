from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_swagger_ui import get_swaggerui_blueprint

db=SQLAlchemy()


def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY']='secret'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///my_db.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL,API_URL,config={'app_name':'TaskAPI'})


    db.init_app(app)
    app.register_blueprint(SWAGGER_BLUEPRINT,url_prefix=SWAGGER_URL)
    from .views import views

    app.register_blueprint(views,url_prefix='/')

    from .models import User, Tasks

    create_db(app)



    return app


def create_db(app):
    if not path.exists('project/my_db.db'):
        db.create_all(app=app)
        print('Database created')