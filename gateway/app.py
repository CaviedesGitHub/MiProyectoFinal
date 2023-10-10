from gateway import create_app
from gateway.vistas.vistas import VistaPing, VistaEmpresa, VistaEmpresas
from gateway.modelos.modelos import db
from flask_restful import Api
from flask_jwt_extended import JWTManager
from faker import Faker
import random
import os
from flask import current_app

settings_module = 'gateway.config.ProductionConfig'  #os.getenv('APP_SETTINGS_MODULE')
app = create_app('default', settings_module)
app_context=app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
#api.add_resource(VistaPerfiles, '/empresas/proyectos/<int:id_proy>/perfiles')
#api.add_resource(VistaProyecto, '/empresas/proyecto/<int:id_proy>')
#api.add_resource(VistaProyectos, '/empresas/<int:id_emp>/proyectos')
#api.add_resource(VistaEmpresas, '/empresas')
#api.add_resource(VistaEmpresa, '/empresa/<int:id_empresa>')

api.add_resource(VistaEmpresas, '/empresas')
api.add_resource(VistaEmpresa, '/empresa/<int:id_empresa>')
api.add_resource(VistaPing, '/gateway/ping')

jwt = JWTManager(app)
