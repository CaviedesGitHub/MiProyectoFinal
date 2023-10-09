from empresas import create_app
from empresas.vistas.vistas import VistaPing, VistaEmpresa, VistaEmpresas
from empresas.vistas.vistas import VistaProyecto, VistaProyectos, VistaPerfiles
from empresas.modelos.modelos import db, Empresa, Estado
from flask_restful import Api
from flask_jwt_extended import JWTManager
from faker import Faker
import random

app=create_app('default')
app_context=app.app_context()
app_context.push()

db.init_app(app)
db.create_all()


api = Api(app)
"""api.add_resource(VistaPerfilCandidato, '/candidato/perfil/<int:id_candidato>')
api.add_resource(VistaPerfiles, '/candidatos/perfiles/llenar/<int:bloque>')
api.add_resource(VistaBasic, '/candidatos/basicas/llenar')
api.add_resource(VistaDatos, '/candidatos/llenar')"""
#api.add_resource(VistaConsultarCandidatos, '/candidatos/consultar')
#api.add_resource(VistaBorrar, '/candidatos/borrar')


#api.add_resource(VistaPerfil, '/empresas/proyectos/<int:id_proy>/perfil/<int:id_perfil>')
api.add_resource(VistaPerfiles, '/empresas/proyectos/<int:id_proy>/perfiles')
api.add_resource(VistaProyecto, '/empresas/proyecto/<int:id_proy>')
api.add_resource(VistaProyectos, '/empresas/<int:id_emp>/proyectos')
api.add_resource(VistaEmpresas, '/empresas')
api.add_resource(VistaEmpresa, '/empresa/<int:id_empresa>')
api.add_resource(VistaPing, '/empresas/ping')


jwt = JWTManager(app)
