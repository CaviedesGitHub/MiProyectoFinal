from flask_restful import Resource
from flask import jsonify
from flask import request
from sqlalchemy import func
from perfiles.modelos.modelos import db, Perfil, HabilPerfil, Habilidad, Nivel_Habil

class VistaPerfil(Resource):
    def get(self, id_perfil):
        print("Obteniendo Perfil")
        lstHabils=db.session.query(Perfil.id, HabilPerfil.valoracion, (Habilidad.id).label('num_habil'), Habilidad.nombre, Habilidad.tipo
           ).filter(Perfil.id==HabilPerfil.id_perfil
           ).filter(HabilPerfil.id_habil==Habilidad.id
           ).filter(Perfil.id==id_perfil).all()
        for h in lstHabils:
            print(h.id, h.num_habil, h.nombre, h.tipo)

        data = []
        for h in lstHabils:
            habil_data = {
                'id_perfil': h.id,
                'id_habil': h.num_habil ,
                'nombre': h.nombre[:-1],
                'tipo_habil': h.tipo.name,
                'cod_habil': h.tipo.value,
                'valoracion': h.valoracion.name
            }
            data.append(habil_data)
        return {'Habilidades': data, 'totalCount': len(data)}, 200
    
class VistaCreaPerfil(Resource):
    def post(self):
        print("Creando Perfil")
        lstHabils=request.json.get("lstHabils")
        if lstHabils is not None and len(lstHabils!=0):
            p=existePerfil(lstHabils)
            if p==0:
                np=creaPerfil(lstHabils)
            else:
                return {"Mensaje":"Perfil ya existe.", "id_perfil":p}, 200    
        else:
            return {"Mensaje":"Falta la lista de habilidades.", "id_perfil":0}, 200
        return {"Mensaje":"Nuevo Perfil creado.", "id_perfil":np}, 200 

class VistaCreaPerfilPlus(Resource):
    def post(self):
        print("Creando Perfil Plus")
        id_perfil=request.json.get("id_perfil")
        lstHabils=request.json.get("lstHabils")
        if lstHabils is not None and id_perfil is not None:
            lstHabilsPerfil=db.session.query(Perfil.id, HabilPerfil.id_habil, HabilPerfil.valoracion
            ).filter(Perfil.id==HabilPerfil.id_perfil
            ).filter(Perfil.id==id_perfil).all()
            lstHabilsCombinada=[]
            for h in lstHabilsPerfil:
                lstHabilsCombinada.append(h.id_habil)
            for h in lstHabils:
                if h not in lstHabilsCombinada:
                    lstHabilsCombinada.append(h)

            p=existePerfil(lstHabilsCombinada)
            if p==0:
                np=creaPerfil(lstHabilsCombinada)
            else:
                return {"Mensaje":"Perfil ya existe.", "id_perfil":p}, 200    
        else:
            return {"Mensaje":"Falta la lista de habilidades o el id de Perfil."}, 200
        return {"Mensaje":"Nuevo Perfil creado.", "id_perfil":np}, 200 

class VistaConsultaPerfil(Resource):
    def get(self):
        print("Consulta Perfil")
        lstHabils=request.json.get("lstHabils")
        if lstHabils is not None:
            p=existePerfil(lstHabils)
            if p==0:
                return {"Mensaje":"Perfil NO existe.", "id_perfil":p}, 200    
            else:
                return {"Mensaje":"Perfil ya existe.", "id_perfil":p}, 200    
        else:
            return {"Mensaje":"Falta la lista de habilidades."}, 200

class VistaConsultaPefiles(Resource):
    def post(self):
        print("Consulta Perfiles.")
        lstHabils=request.json.get("lstHabils")
        if lstHabils is not None:
            long_lista=len(lstHabils)
            conteo=(func.count(HabilPerfil.id_perfil)).label('conteo')
            lstCumplenHabils = db.session.query(HabilPerfil.id_perfil, HabilPerfil.id_habil, HabilPerfil.valoracion).filter(HabilPerfil.id_perfil.in_(db.session.query(HabilPerfil.id_perfil).filter(HabilPerfil.id_habil.in_(lstHabils)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista)))
            for h in lstCumplenHabils:
                print(h)
            num_perfil=0
            data1 = []
            data = []
            for h in lstCumplenHabils:
                if h.id_perfil!=num_perfil:
                    if num_perfil!=0:
                        resp={
                            'id_perfil': num_perfil, 
                            'lstHabils': data 
                        }
                        data1.append(resp)
                        data = []
                    num_perfil=h.id_perfil
                habil_data = {
                    'id_perfil': h.id_perfil,
                    'id_habil': h.id_habil,
                    'valoracion': h.valoracion.name,
                    'cod_valor': h.valoracion.value
                }
                data.append(habil_data)
            resp={
                    'id_perfil': num_perfil, 
                    'lstHabils': data 
            }
            data1.append(resp)
            return {'ListaPerfiles': data1, 'totalCount': len(data1)}, 200
        else:
            return {"Mensaje":"Falta la lista de habilidades."}, 200


class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong"}, 200


def existePerfil(lstHabilidades):
    long_lista=len(lstHabilidades)
    conteo=(func.count(HabilPerfil.id_perfil)).label('conteo')
    queryCumplenHabils=db.session.query(HabilPerfil.id_perfil, conteo).filter(HabilPerfil.id_habil.in_(lstHabilidades)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all()
    if len(queryCumplenHabils)==0:
       return 0
    else:
       queryLongCorrecta=db.session.query(HabilPerfil.id_perfil, conteo).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all()    
       for h in queryCumplenHabils:
            for hh in queryLongCorrecta:
                if h.id_perfil==hh.id_perfil:
                   return h.id_perfil
       return 0

def creaPerfil(lsthabil):
    try:
        np=Perfil()
        db.session.add(np)
        db.session.commit()
        for h in lsthabil:
            nhp=HabilPerfil()
            nhp.id_habil=h
            nhp.id_perfil=np.id
            nhp.valoracion=Nivel_Habil.BAJO
            db.session.add(nhp)
            db.session.commit()
        return np.id
    except Exception as inst:
        db.session.rollback()
        print(type(inst))    # the exception instance
        #print(inst)
        print("habilidad no se pudo crear.")