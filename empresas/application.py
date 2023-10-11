from flask_restful import Api
from flask_jwt_extended import JWTManager
from faker import Faker
import random
import os


from flask import Flask
import os
def create_app(config_name, settings_module='config.ProductionConfig'):
    app=Flask(__name__)
    app.config.from_object(settings_module)
    return app

settings_module = os.getenv('APP_SETTINGS_MODULE','config.ProductionConfig')
application = create_app('default', settings_module)
app_context=application.app_context()
app_context.push()



import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime, Date
from sqlalchemy.sql import func

db = SQLAlchemy()

class Estado(enum.Enum):
    ACTIVO = 1
    INACTIVO = 2

class Nivel_Estudios(enum.Enum):
    PREGRADO = 1
    ESPECIALIZACION = 2
    MAESTRIA = 3
    DOCTORADO = 4
    DIPLOMADOS = 5
    CURSOS = 6

class Empresa(db.Model):
    __tablename__ = 'empresas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING', unique=True)
    tipo = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    correo = db.Column(db.Unicode(128), nullable=False, unique=True)
    celular = db.Column(db.Unicode(128), nullable=True)
    contacto = db.Column(db.Unicode(128), default='MISSING')
    pais = db.Column(db.Unicode(128))
    ciudad = db.Column(db.Unicode(128))
    direccion = db.Column(db.Unicode(128))
    id_usuario = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True)
    estado = db.Column(db.Enum(Estado), nullable=False, default=Estado.ACTIVO)  

    def __init__(self, *args, **kw):
        super(Empresa, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Empresa.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Empresa.query.filter_by(email=email).first()

    @staticmethod
    def get_count():
        return Empresa.query.count()

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        else:
            return value.name #{'llave':value.name, 'valor':value.value} #{value.name}  #{'llave':value.name, 'valor':value.value}
    
class EmpresaSchema(SQLAlchemyAutoSchema):
    estado=EnumADiccionario(attribute=('estado'))
    class Meta:
        model = Empresa
        include_relationships = True
        load_instance = True

empresa_schema = EmpresaSchema()


class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_emp = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    descripcion = db.Column(db.Unicode(128), nullable=False, default='MISSING')


    def __init__(self, *args, **kw):
        super(Proyecto, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Proyecto.query.get(id)

    @staticmethod
    def get_by_empresa(id_emp):
        return Proyecto.query.filter(Proyecto.id_emp==id_emp).all()

 
class ProyectoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Proyecto
        include_relationships = True
        load_instance = True

proyecto_schema = ProyectoSchema()


class PerfilesProyecto(db.Model):
    __tablename__ = 'perfiles_proyectos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    id_proy = db.Column(db.Integer, nullable=False)
    id_perfil = db.Column(db.Integer, nullable=False)
    id_cand = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, *args, **kw):
        super(PerfilesProyecto, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return PerfilesProyecto.query.get(id)

    @staticmethod
    def get_count():
        return PerfilesProyecto.query.count()

    
class PerfilesProyectoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PerfilesProyecto
        include_relationships = True
        load_instance = True

perfiles_proyecto_schema = PerfilesProyectoSchema()


class EmpleadoEmpresa(db.Model):
    __tablename__ = 'empleado_empresa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_emp = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    id_perfil = db.Column(db.Integer, nullable=True)


    def __init__(self, *args, **kw):
        super(EmpleadoEmpresa, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return EmpleadoEmpresa.query.get(id)

 
class EmpleadoEmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmpleadoEmpresa
        include_relationships = True
        load_instance = True

empleado_empresa_schema = EmpleadoEmpresaSchema()


class Encargado(db.Model):
    __tablename__ = 'encargado'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_proy = db.Column(db.Integer, nullable=False)
    id_empleado = db.Column(db.Integer, nullable=False)
    rol = db.Column(db.Unicode(128), nullable=False, default='MISSING')


    def __init__(self, *args, **kw):
        super(Encargado, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Encargado.query.get(id)

 
class EncargadoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Encargado
        include_relationships = True
        load_instance = True

encargado_schema = EncargadoSchema()

db.init_app(application)
db.create_all()




from datetime import datetime
from datetime import timedelta
import math
import random
import uuid
from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
#from empresas.modelos.modelos import db, Empresa, EmpresaSchema, Estado, Proyecto, ProyectoSchema
#from empresas.modelos.modelos import PerfilesProyecto, PerfilesProyectoSchema
from sqlalchemy import desc, asc

import os
import requests
import json
from faker import Faker

empresa_schema = EmpresaSchema()
proyecto_schema = ProyectoSchema()
perfilesproyecto_schema = PerfilesProyectoSchema()

access_token_expires = timedelta(minutes=120)

class VistaEmpresas(Resource):
    def post(self):
        print("Creando Empresa")
        try:
            ne=Empresa()
            ne.nombre=request.json.get("nombre")
            ne.correo=request.json.get("correo")
            ne.tipo=request.json.get("tipo")
            ne.pais=request.json.get("pais")
            ne.ciudad=request.json.get("ciudad")
            ne.direccion=request.json.get("direccion")
            ne.contacto=request.json.get("contacto")
            ne.celular=request.json.get("celular")
            ne.estado=Estado[request.get_json()['estado']]
            ne.is_active=request.json.get("is_active")
            ne.id_usuario=request.json.get("id_usuario")
            db.session.add(ne)
            db.session.commit()
            return {"Empresa nueva: ":empresa_schema.dump(ne)}, 200
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("Empresa no se pudo crear.")
            return {"Mensaje: ":"Error: Empresa no se pudo crear."}, 200
    
    def get(self):
        print("Listar Empresas")
        #user_jwt=int(get_jwt_identity())  
        #max=request.json.get("max", 50)
        #if request.get_json()['order']=="ASC":
        #   return  [tarea_schema.dump(tar) for tar in Tarea.query.filter(Tarea.id_usr==user_jwt).order_by(Tarea.fecha.asc()).paginate(page=1, per_page=max, error_out=False)] 
        #else:
        #   return  [tarea_schema.dump(tar) for tar in Tarea.query.filter(Tarea.id_usr==user_jwt).order_by(Tarea.fecha.desc()).paginate(page=1, per_page=max, error_out=False)]  
        return 200

class VistaEmpresa(Resource):
    def get(self, id_empresa):
        print("Consultar Empresa")
        try:
            empresa = Empresa.query.get_or_404(id_empresa)
            return empresa_schema.dump(empresa)
        except Exception as inst:
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion de la Empresa.")
            return {"Mensaje: ":"Error: No se pudo obtener la informacion de la Empresa."}, 200

class VistaProyectos(Resource):
    def post(self, id_emp):
        print("Crear Proyecto")
        emp=Empresa.get_by_id(id_emp)
        if emp is not None:
            try:
                np=Proyecto()
                np.nombre=request.json.get("nombre")
                np.id_emp=id_emp
                np.descripcion=request.json.get("descripcion")
                db.session.add(np)
                db.session.commit()
                return {"Proyecto nuevo: ":proyecto_schema.dump(np)}, 200
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                #print(inst)
                print("Proyecto no se pudo crear.")
                return {"Mensaje: ":"Error: Proyecto no se pudo crear."}, 200
        else:
            return {"Mensaje: ":"Error: Proyecto no se pudo crear. La empresa no existe."}, 200

    def get(self, id_emp):
        print("Consultar Proyectos de una Empresa")
        try:
            return  [proyecto_schema.dump(p) for p in Proyecto.get_by_empresa(id_emp)]  
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion de los Proyectos.")
            return {"Mensaje: ":"Error: No se pudo obtener la informacion de los Proyectos."}, 200

class VistaProyecto(Resource):
    def get(self, id_proy):
        print("Consultar Proyecto")
        try:
            proyecto = Proyecto.query.get_or_404(id_proy)
            return proyecto_schema.dump(proyecto)
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion del Proyecto.")
            return {"Mensaje: ":"Error: No se pudo obtener la informacion del Proyecto."}, 200

class VistaPerfiles(Resource):
    def post(self, id_proy):
        print("Crear perfil de Proyecto")
        proy=Proyecto.get_by_id(id_proy)
        if proy is not None:
            try:
                headers={}
                body=request.json.get("lstHabils")
                response = send_post_request(f"{current_app.config['HOST_PORT_PERFILES']}/perfil/crear", headers=headers, body=body)
                print(response) 
                if response.get("id_perfil")!=0:
                    npp=PerfilesProyecto()
                    npp.nombre=request.json.get("nombre")
                    npp.id_cand=0
                    npp.id_proy=id_proy
                    npp.id_perfil=response.get("id_perfil")
                    db.session.add(npp)
                    db.session.commit()
                    return {"Perfil nuevo: ":perfilesproyecto_schema.dump(npp)}, 200
                else:
                    return {"Mensaje: ":"Error: Perfil no se pudo crear."}, 200    
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                #print(inst)
                print("Perfil no se pudo crear.")
                return {"Mensaje: ":"Error: Perfil no se pudo crear."}, 200
        else:
            return {"Mensaje: ":"Error: Perfil no se pudo crear. El proyecto no existe."}, 200

class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong"}, 200

def send_post_request(url, headers, body):
    try:
        response = requests.post(url, json=body, headers=headers, timeout=5000)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as inst:
        print(type(inst))
        #print(inst)
        return -1

api = Api(application)
api.add_resource(VistaPerfiles, '/empresas/proyectos/<int:id_proy>/perfiles')
api.add_resource(VistaProyecto, '/empresas/proyecto/<int:id_proy>')
api.add_resource(VistaProyectos, '/empresas/<int:id_emp>/proyectos')
api.add_resource(VistaEmpresas, '/empresas')
api.add_resource(VistaEmpresa, '/empresa/<int:id_empresa>')
api.add_resource(VistaPing, '/empresas/ping')


jwt = JWTManager(application)
