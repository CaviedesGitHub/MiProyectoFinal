#from candidato import create_app
#from candidato.vistas.vistas import VistaPing, VistaBorrar, VistaCandidatosPerfiles, VistaCandidato
#from candidato.modelos.modelos import db, Candidato, Estado
from flask_restful import Api
from flask_jwt_extended import JWTManager
from faker import Faker
import random
import os

from flask import Flask
def create_app(config_name, settings_module='config.ProductionConfig'):
    app=Flask(__name__)
    app.config.from_object(settings_module)
    return app

"""def create_app(config_name):
    app=Flask(__name__)
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'Proyecto2023'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    if 'RDS_HOSTNAME' in os.environ:
        NAME=os.environ['RDS_DB_NAME']
        USER=os.environ['RDS_USERNAME']
        PASSWORD=os.environ['RDS_PASSWORD']
        HOST=os.environ['RDS_HOSTNAME']
        PORT=os.environ['RDS_PORT']
        app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/CandidatosBD'      
    return app                                   """

settings_module = os.getenv('APP_SETTINGS_MODULE','config.ProductionConfig')
application = create_app('default', settings_module)
#application = create_app('default')
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

class Candidato(db.Model):
    __tablename__ = 'candidato'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    apellidos = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    documento = db.Column(db.Integer, nullable=False, unique=True)
    fecha_nac = db.Column(Date(), nullable=True)
    email = db.Column(db.Unicode(128), nullable=False, unique=True)
    phone = db.Column(db.Unicode(128))
    ciudad = db.Column(db.Unicode(128))
    direccion = db.Column(db.Unicode(128))
    num_perfil = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True)
    estado = db.Column(db.Enum(Estado), nullable=False, default=Estado.ACTIVO)  

    def __init__(self, *args, **kw):
        super(Candidato, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Candidato.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Candidato.query.filter_by(email=email).first()

    @staticmethod
    def get_count():
        return Candidato.query.count()

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        else:
            return value.name #{'llave':value.name, 'valor':value.value} #{value.name}  #{'llave':value.name, 'valor':value.value}
    
class CandidatoSchema(SQLAlchemyAutoSchema):
    estado=EnumADiccionario(attribute=('estado'))
    class Meta:
        model = Candidato
        include_relationships = True
        load_instance = True

candidato_schema = CandidatoSchema()


class Datos_Laborales(db.Model):
    __tablename__ = 'datos_laborales'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_cand = db.Column(db.Integer, nullable=False)

    empresa = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    cargo = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    funciones = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    fecha_ing = db.Column(Date(), nullable=True)
    fecha_sal = db.Column(Date(), nullable=True)

    def __init__(self, *args, **kw):
        super(Datos_Laborales, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Datos_Laborales.query.get(id)

 
class Datos_LaboralesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Datos_Laborales
        include_relationships = True
        load_instance = True

datos_laborales_schema = Datos_LaboralesSchema()



class Datos_Academicos(db.Model):
    __tablename__ = 'datos_academicos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_cand = db.Column(db.Integer, nullable=False)
    institucion = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    titulo = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    anio = db.Column(db.Integer, nullable=False, default=2023)
    nivel = db.Column(db.Enum(Nivel_Estudios), nullable=False, default=Nivel_Estudios.CURSOS)  

    def __init__(self, *args, **kw):
        super(Datos_Academicos, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Datos_Academicos.query.get(id)

    @staticmethod
    def get_count():
        return Datos_Academicos.query.count()

    
class Datos_AcademicosSchema(SQLAlchemyAutoSchema):
    nivel=EnumADiccionario(attribute=('nivel'))
    class Meta:
        model = Datos_Academicos
        include_relationships = True
        load_instance = True

datos_academicos_schema = Datos_AcademicosSchema()

db.init_app(application)
db.create_all()



from datetime import datetime
from datetime import timedelta
import math
import random
import uuid
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
#from candidato.modelos.modelos import db, Candidato, CandidatoSchema, Estado
from sqlalchemy import desc, asc

import os
#import requests
import json
from faker import Faker

candidato_schema = CandidatoSchema()
access_token_expires = timedelta(minutes=120)

class VistaBorrar(Resource):
    def delete(self):
        print("Borrando Datos.")
        lstCandidatos=Candidato.query.all()
        registros=0
        for c in lstCandidatos:
            try:
                db.session.delete(c)
                db.session.commit()
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                #print(inst)
                print("registro no se pudo borrar.")
        return {"Mensaje":"registros borrados: "+str(registros)}, 200

class VistaCandidato(Resource):
    def get(self, id_cand):
        print("Consultar Candidato")
        try:
            candidato = Candidato.query.get_or_404(id_cand)
            return candidato_schema.dump(candidato)
        except Exception as inst:
            print(type(inst))    # the exception instance
            #print(inst)
            print("No se pudo obtener la informacion del candidato.")
            return {"Mensaje: ":"Error: No se pudo obtener la informacion del candidato."}, 200

class VistaCandidatosPerfiles(Resource):
    def post(self):
        print("Seleccion de candidatos segun perfiles")
        lstPerfiles=request.json.get("lstPerfiles")
        print(lstPerfiles)
        lstCandidatos = db.session.query(Candidato.id, Candidato.nombres, Candidato.apellidos, Candidato.num_perfil).filter(Candidato.num_perfil.in_(lstPerfiles)).order_by(asc(Candidato.num_perfil)).all()
        data = []
        for c in lstCandidatos:
            cand_data = {
                'id_cand': c.id,
                'nombres': c.nombres,
                'apellidos': c.apellidos,
                'id_perfil': c.num_perfil
            }
            data.append(cand_data)
        return {'Candidatos': data, 'totalCount': len(data)}, 200


class VistaRaiz(Resource):
    def get(self):
        print("Hola")
        return {"Mensaje":"Hola, Bienvenido De Nuevo v3.3 Inmutable"}, 200

class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong version 3.3 Inmutable"}, 200

class VistaEnv(Resource):
    def get(self):
        print("Environment")
        return {
            "RDS_DB_NAME":os.environ['RDS_DB_NAME'],
            "RDS_USERNAME":os.environ['RDS_USERNAME'],
            "RDS_PASSWORD":os.environ['RDS_PASSWORD'],
            "RDS_HOSTNAME":os.environ['RDS_HOSTNAME'],
            "RDS_PORT":os.environ['RDS_PORT'],
            "URL_DATABASE":application.config['SQLALCHEMY_DATABASE_URI'],
        }, 200

api = Api(application)
api.add_resource(VistaRaiz, '/')
api.add_resource(VistaEnv, '/env')
api.add_resource(VistaBorrar, '/candidatos/borrar')
api.add_resource(VistaCandidatosPerfiles, '/candidatos/perfiles')
api.add_resource(VistaCandidato, '/candidato/<int:id_cand>')
api.add_resource(VistaPing, '/candidato/ping')


jwt = JWTManager(application)


print("From application.py")
print(settings_module)

if Candidato.get_count()==0:
    faker=Faker(['es_CO'])
    registros=0
    for i in range(500):
        try:
            cn=Candidato()
            cn.nombres=faker.first_name()
            cn.apellidos=faker.last_name()
            cn.documento=faker.unique.random_int(min=1000000, max=2000000000) 
            cn.direccion=faker.street_address()
            cn.ciudad=faker.city()
            cn.email=faker.email()
            cn.phone=faker.phone_number()
            cn.fecha_nac=faker.date_between(start_date= "-80y" ,end_date= "-18y" )
            cn.estado=Estado.ACTIVO
            cn.num_perfil=(registros+1) % 250  #random.randint(1, 300)
            db.session.add(cn)
            db.session.commit()
            registros=registros+1
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("registro no se pudo guardar.")
    
    faker=Faker(['en_US'])
    for i in range(300):
        try:
            cn=Candidato()
            cn.nombres=faker.first_name()
            cn.apellidos=faker.last_name()
            cn.documento=faker.unique.random_int(min=1000000, max=2000000000) 
            cn.direccion=faker.street_address()
            cn.ciudad=faker.city()
            cn.email=faker.email()
            cn.phone=faker.phone_number()
            cn.fecha_nac=faker.date_between(start_date= "-80y" ,end_date= "-18y" )
            cn.estado=Estado.ACTIVO
            cn.num_perfil=(registros+1) % 250  #random.randint(1, 300)
            db.session.add(cn)
            db.session.commit()
            registros=registros+1
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("registro no se pudo guardar.")
    
    faker=Faker(['it_IT'])
    for i in range(200):
        try:
            cn=Candidato()
            cn.nombres=faker.first_name()
            cn.apellidos=faker.last_name()
            cn.documento=faker.unique.random_int(min=1000000, max=2000000000) 
            cn.direccion=faker.street_address()
            cn.ciudad=faker.city()
            cn.email=faker.email()
            cn.phone=faker.phone_number()
            cn.fecha_nac=faker.date_between(start_date= "-80y" ,end_date= "-18y" )
            cn.estado=Estado.ACTIVO
            cn.num_perfil=(registros+1) % 250  #random.randint(1, 300)
            db.session.add(cn)
            db.session.commit()
            registros=registros+1
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("registro no se pudo guardar.")

#if __name__ == "__main__":
#    application.run(port = 5000, debug = True)