from candidato import create_app
from candidato.vistas.vistas import VistaPing, VistaBorrar
from candidato.modelos.modelos import db, Candidato, Estado
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
api.add_resource(VistaBorrar, '/candidatos/borrar')
api.add_resource(VistaPing, '/candidato/ping')


jwt = JWTManager(app)

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
            cn.num_perfil=random.randint(1, 300)
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
            cn.num_perfil=random.randint(1, 300)
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
            cn.num_perfil=random.randint(1, 300)
            db.session.add(cn)
            db.session.commit()
            registros=registros+1
        except Exception as inst:
            db.session.rollback()
            print(type(inst))    # the exception instance
            #print(inst)
            print("registro no se pudo guardar.")
