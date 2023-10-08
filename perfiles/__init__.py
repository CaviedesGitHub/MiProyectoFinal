import datetime
from flask import Flask
import os

def create_app(config_name):
    app=Flask(__name__)
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

    container=os.getenv("CONTAINER")
    if container=='SI':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("POSTGRES_URL")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/PerfilesBD'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'proyecto2_2023'
    #app.config["JWT_ACCESS_TOKEN_EXPIRES"] = True
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    return app