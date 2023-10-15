from auth import create_app
from auth.vistas.vistas import VistaPing, VistaLogIn, VistaSignIn, VistaUsuario, VistaAuthorization
from auth.modelos.modelos import db, Usuario, UserType
from flask_restful import Api
from flask_jwt_extended import JWTManager
import random
import os

settings_module = os.getenv('APP_SETTINGS_MODULE','config.ProductionConfig')
app = create_app('default', settings_module)
app_context=app.app_context()
app_context.push()


db.init_app(app)
db.create_all()


api = Api(app)
api = Api(app)
api.add_resource(VistaSignIn, '/auth/signup')
api.add_resource(VistaLogIn, '/auth/login')
api.add_resource(VistaUsuario, '/usuario/<int:id_usuario>')
api.add_resource(VistaAuthorization, '/auth/me')
api.add_resource(VistaPing, '/auth/ping')


jwt = JWTManager(app)