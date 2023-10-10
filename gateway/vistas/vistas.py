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
import requests
import json
from faker import Faker

#################################################################################
####################################   EMPRESAS   ###############################
#################################################################################

class VistaPerfiles(Resource):
    def post(self, id_proy):
        headers=request.headers
        body=request.json
        response = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, 200
        
class VistaProyecto(Resource):
    def get(self, id_proy):
        headers={}
        response = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, 200


class VistaProyectos(Resource):
    def post(self, id_emp):
        headers=request.headers
        body=request.json
        response = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, 200

    def get(self, id_emp):
        headers={}
        response = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, 200


class VistaEmpresas(Resource):
    def post(self):
        headers=request.headers
        body=request.json
        response = send_post_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                           body=body, headers=headers, tiempoespera=5000)
        return response, 200
    
    def get(self):
        headers={}
        response = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, 200

class VistaEmpresa(Resource):
    def get(self, id_empresa):        
        headers=request.headers
        response = send_get_request(url=f"{current_app.config['HOST_PORT_EMPRESA']}{request.path}",
                                 headers=headers, tiempoespera=5000)
        return response, 200

#################################################################################
#################################   FIN EMPRESAS   ##############################
#################################################################################

class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong"}, 200


def send_post_request(url, headers, body, tiempoespera):
    try:
        response = requests.post(url, json=body, headers=headers, timeout=tiempoespera)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as inst:
        print(type(inst))
        #print(inst)
        return -1

def send_get_request(url, headers, tiempoespera):
    print(url)
    try:
        response = requests.get(url=url, headers=headers, timeout=tiempoespera)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as inst:
        print(type(inst))
        #print(inst)
        return -1