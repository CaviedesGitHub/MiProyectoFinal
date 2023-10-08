from datetime import datetime
from datetime import timedelta
import math
import random
import uuid
from flask import request, copy_current_request_context, redirect
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import os
import requests
import json
from time import sleep
import threading
import concurrent.futures

num_request=0


class VistaPerfil(Resource):
    def post(self):
        print("perfil")
        global num_request
        num_request=num_request+1

        perfil=request.json

        headers={} #headers = {"Authorization": f"Bearer {os.environ.get('TRUE_NATIVE_TOKEN')}"}
        body=perfil #{} #body = {"user": user_data, "transactionIdentifier": str(uuid.uuid4()), "userIdentifier": str(id),
            #"userWebhook": f"http://{os.environ.get('USERS_MS')}/users/verification-webhook"} 

        response = send_post_request(f"http://127.0.0.1:5000/perfil/consultar/perfiles",
                                 headers=headers, body=body)
        print(response)     
        #@copy_current_request_context
        def ctx_bridge(candidatos, id_motor, url, num_rq):
            return(solicitud_motor(candidatos, id_motor, url, num_rq))

        result1={}
        result2={}
        result3={}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futuro1=executor.submit(ctx_bridge, response, 1, "http://127.0.0.1:5002/motor/emparejar", num_request)
            futuro2=executor.submit(ctx_bridge, response, 2, "http://127.0.0.1:5003/motor/emparejar", num_request)
            futuro3=executor.submit(ctx_bridge, response, 3, "http://127.0.0.1:5004/motor/emparejar", num_request)

            result1=futuro1.result()
            result2=futuro2.result()
            result3=futuro3.result()

            if (result1==-1 or result1 is None) and (result2==-1 or result2 is None) and (result3==-1 or result3 is None):
                return {"Mensaje":"Error en el Motor de Emparejamiento."}, 200
            elif (result1==-1 or result1 is None) and (result2==-1 or result2 is None):
                Lst_Perfiles=result3.get('Perfiles')
            elif (result1==-1 or result1 is None) and (result3==-1 or result3 is None):
                Lst_Perfiles=result2.get('Perfiles')
            elif (result2==-1 or result2 is None) and (result3==-1 or result3 is None):
                Lst_Perfiles=result1.get('Perfiles')
            elif (result1==-1 or result1 is None):
                if result2.get('Perfiles')==result3.get('Perfiles'):
                    Lst_Perfiles=result2.get('Perfiles')
                else:
                    common = set(result2.get('Perfiles')).intersection(result3.get('Perfiles'))
                    Lst_Perfiles=list(common)
            elif (result2==-1 or result2 is None):
                if result1.get('Perfiles')==result3.get('Perfiles'):
                    Lst_Perfiles=result1.get('Perfiles')
                else:
                    common = set(result1.get('Perfiles')).intersection(result3.get('Perfiles'))
                    Lst_Perfiles=list(common)
            elif (result3==-1 or result3 is None):
                if result1.get('Perfiles')==result2.get('Perfiles'):
                    Lst_Perfiles=result1.get('Perfiles')
                else:
                    common = set(result1.get('Perfiles')).intersection(result2.get('Perfiles'))
                    Lst_Perfiles=list(common)
            else:
                if result1.get('Perfiles')==result2.get('Perfiles') and result2.get('Perfiles')==result3.get('Perfiles'):
                    Lst_Perfiles=result1.get('Perfiles')
                elif result1.get('Perfiles')==result2.get('Perfiles'):
                    Lst_Perfiles=result1.get('Perfiles')
                elif result1.get('Perfiles')==result3.get('Perfiles'):
                    Lst_Perfiles=result1.get('Perfiles')
                elif result2.get('Perfiles')==result3.get('Perfiles'):
                    Lst_Perfiles=result2.get('Perfiles')
                else:
                    common = set(result1.get('Perfiles')).intersection(result2.get('Perfiles'))
                    common = common.intersection(result3.get('Perfiles'))
                    Lst_Perfiles=list(common)

        for pp in Lst_Perfiles:
            print(pp) 

        Lst_Resp=[]
        for p in Lst_Perfiles:
            Id_Perfil=p.get("id_perfil")
            Cal=p.get("Calificacion")
            if Cal>70:
                Dict_Perfil={}
                Dict_Perfil["Id_Perfil"]=Id_Perfil
                Dict_Perfil["Calificacion"]=Cal
                Lst_Resp.append(Dict_Perfil)
        return {"Seleccion":Lst_Resp}, 200

def solicitud_motor(candidatos, id_motor, url, num_rq):
    headers={} #headers = {"Authorization": f"Bearer {os.environ.get('TRUE_NATIVE_TOKEN')}"}
    body=candidatos #body = {"user": user_data, "transactionIdentifier": str(uuid.uuid4()), "userIdentifier": str(id),
        #"userWebhook": f"http://{os.environ.get('USERS_MS')}/users/verification-webhook"}

    for i in range(3):
        response = send_post_request(url, headers=headers, body=body)
        if response==-1:
            print("Error en Motor No. ", id_motor, ". Motor NO Disponible.")
            reg_log(num_request, id_motor, i+1, "Error. Motor NO disponible.")
        elif response is None:
            print("Error en Motor No. ", id_motor, ". Codigo de respuesta diferente de 200.")
            reg_log(num_request, id_motor, i+1, "Error. Codigo de respuesta diferente de 200.")
        else:
            print("Respuesta obtenida de Motor No. ", id_motor)
            reg_log(num_request, id_motor, i+1, "Exito. Respuesta generada..")
            break
    #print(response)
    return response

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

def send_get_request(url, headers):
    response = requests.get(url=url, headers=headers, timeout=5000)
    return response.json()

def reg_log(num_rq, num_motor, intento, msg):
    fecha_hora_actual = datetime.now()
    fecha_hora_como_cadena = fecha_hora_actual.strftime("%Y-%m-%d;%H:%M:%S")
    with open('log_validador.txt', 'a') as f:
        f.write(f"{fecha_hora_como_cadena}; Peticion: {num_rq}; Motor: {num_motor}; Intento:{intento}; Msg: {msg}")
        f.write('\n')


class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong"}, 200