from datetime import datetime
from datetime import timedelta
import math
import random
import uuid
from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from empresas.modelos.modelos import db, Empresa, EmpresaSchema, Estado, Proyecto, ProyectoSchema
from empresas.modelos.modelos import PerfilesProyecto, PerfilesProyectoSchema
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