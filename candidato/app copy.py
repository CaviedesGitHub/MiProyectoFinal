from candidato import create_app
from candidato.vistas.vistas import VistaPing, VistaBorrar, VistaCandidatosPerfiles, VistaCandidato, VistaEnv, VistaRaiz
from candidato.modelos.modelos import db, Candidato, Estado
from flask_restful import Api
from flask_jwt_extended import JWTManager
from faker import Faker
import random
import os


settings_module = os.getenv('APP_SETTINGS_MODULE','config.ProductionConfig')
application = create_app('default', settings_module)
#application = create_app('default')
app_context=application.app_context()
app_context.push()

db.init_app(application)
db.create_all()

api = Api(application)
api.add_resource(VistaRaiz, '/')
api.add_resource(VistaEnv, '/env')
api.add_resource(VistaBorrar, '/candidatos/borrar')
api.add_resource(VistaCandidatosPerfiles, '/candidatos/perfiles')
api.add_resource(VistaCandidato, '/candidato/<int:id_cand>')
api.add_resource(VistaPing, '/candidato/ping')


jwt = JWTManager(application)

print("From app.py")
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