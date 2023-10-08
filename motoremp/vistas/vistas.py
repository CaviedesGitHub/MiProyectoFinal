from datetime import datetime
from datetime import timedelta
import math
import random
import uuid
from flask import request, copy_current_request_context
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import os
import json
from faker import Faker
from time import sleep
import threading
import concurrent.futures


class VistaEmparejar(Resource):
    def post(self):
        print("Emparejando")
        print(request.json)
        lstPerfiles=request.json.get("ListaPerfiles")
        for p in lstPerfiles:
            calificacion=random.randint(70, 100)
            p["Calificacion"]=calificacion
        #print(lstPerfiles)
        print(sorted(lstPerfiles, key=lambda i: i['Calificacion'], reverse=True))
        lstPerfiles=sorted(lstPerfiles, key=lambda i: i['Calificacion'], reverse=True)
        return {"Perfiles":lstPerfiles}, 200 #{"Mensaje":"Emparejar"}, 200

class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong"}, 200
