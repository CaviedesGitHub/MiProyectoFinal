from datetime import datetime
from datetime import timedelta
import math
import random
import uuid
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from candidato.modelos.modelos import db, Candidato, CandidatoSchema, Estado

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

class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong"}, 200

