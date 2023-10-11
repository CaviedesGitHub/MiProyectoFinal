from datetime import datetime
from datetime import timedelta
import math
import random
import uuid
from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from candidato.modelos.modelos import db, Candidato, CandidatoSchema, Estado
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

class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong"}, 200

class VistaRaiz(Resource):
    def get(self):
        print("Hola")
        return {"Mensaje":"Hola, Bienvenido De Nuevo v3.3 Inmutable"}, 200

class VistaEnv(Resource):
    def get(self):
        print("Environment")
        return {
            "RDS_DB_NAME":os.environ['RDS_DB_NAME'],
            "RDS_USERNAME":os.environ['RDS_USERNAME'],
            "RDS_PASSWORD":os.environ['RDS_PASSWORD'],
            "RDS_HOSTNAME":os.environ['RDS_HOSTNAME'],
            "RDS_PORT":os.environ['RDS_PORT'],
            "URL_DATABASE":current_app.config['SQLALCHEMY_DATABASE_URI'],
        }, 200