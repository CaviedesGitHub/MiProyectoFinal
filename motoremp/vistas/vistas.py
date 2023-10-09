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
import requests


class VistaEmparejar(Resource):
    def post(self):
        print("Emparejando")
        #print(request.json)
        lstPerfiles=request.json.get("ListaPerfiles")
        lstIdPerfiles=[]
        for p in lstPerfiles:
            calificacion=random.randint(70, 100)
            p["Calificacion"]=calificacion
            lstIdPerfiles.append(p.get('id_perfil'))
        
        print(lstIdPerfiles)
        #lstIdPerfiles=[1,3,5,9]
        headers={} 
        body={"lstPerfiles":lstIdPerfiles}
        response = send_post_request(f"http://127.0.0.1:5004/candidatos/perfiles",
                                 headers=headers, body=body)
        lstCandidatos=response.get("Candidatos")
        for p in lstPerfiles:
            print(p)
            for c in lstCandidatos:
                print("c", c)
                if p["id_perfil"]==c["id_perfil"]:
                    c["Calificacion"]=p["Calificacion"]

        for c in lstCandidatos:
            print(c)

        for c in lstCandidatos:
            cal_inf=c["Calificacion"]
            c["Calificacion"]=random.randint(cal_inf, 100)
        #print(lstPerfiles)
        print(sorted(lstCandidatos, key=lambda i: i['Calificacion'], reverse=True))
        lstCandidatos=sorted(lstCandidatos, key=lambda i: i['Calificacion'], reverse=True)
        return {"Candidatos":lstCandidatos}, 200 #{"Mensaje":"Emparejar"}, 200

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