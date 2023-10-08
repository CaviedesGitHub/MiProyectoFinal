from perfiles import create_app
from perfiles.vistas.vistas import VistaPing, VistaPerfil, VistaCreaPerfil, VistaCreaPerfilPlus, VistaConsultaPerfil, VistaConsultaPefiles
from perfiles.modelos.modelos import db, Perfil, HabilPerfil, Habilidad, Tipo_Habil, Nivel_Habil
from flask_restful import Api
from flask_jwt_extended import JWTManager
import math
import random
from sqlalchemy import func
from sqlalchemy.orm import aliased

app=create_app('default')
app_context=app.app_context()
app_context.push()

db.init_app(app)
db.create_all()


api = Api(app)
api.add_resource(VistaPing, '/perfiles/ping')
api.add_resource(VistaPerfil, '/perfil/<int:id_perfil>')
api.add_resource(VistaCreaPerfil, '/perfil/crear')
api.add_resource(VistaCreaPerfilPlus, '/perfil/crear/plus')
api.add_resource(VistaConsultaPerfil, '/perfil/consultar')
api.add_resource(VistaConsultaPefiles, '/perfil/consultar/perfiles')


jwt = JWTManager(app)

def queHabil(lstHabil, orden):
    i=1
    for h in lstHabil:
        if i==orden:
            return h.id
        i=i+1
    return None

def adicionarPerfil(lsthabil):
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
    except Exception as inst:
        db.session.rollback()
        print(type(inst))    # the exception instance
        #print(inst)
        print("habilidad no se pudo crear.")


if Habilidad.get_count()==0:
    print("Creando Habilidades.")
    regT=0
    with open("./lenguajes.txt") as archivo:
        for linea in archivo:
            try:
                nombre=linea.split(sep=',')[1]
                nh=Habilidad()
                nh.nombre=nombre
                nh.tipo=Tipo_Habil.TECNICA
                db.session.add(nh)
                db.session.commit()
                regT=regT+1
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                #print(inst)
                print("habil tecnica no se pudo crear.")
    regB=0
    with open("./habilblandas.txt") as archivo:
        for linea in archivo:
            try:
                nombre=linea.split(sep=':')[1]
                nh=Habilidad()
                nh.nombre=nombre
                nh.tipo=Tipo_Habil.BLANDA
                db.session.add(nh)
                db.session.commit()
                regB=regB+1
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                #print(inst)
                print("habil blanda no se pudo crear.")
    regP=0
    with open("./personalidad.txt") as archivo:
        for linea in archivo:
            try:
                nombre=linea.split(sep=',')[1]
                nh=Habilidad()
                nh.nombre=nombre
                nh.tipo=Tipo_Habil.PERSONALIDAD
                db.session.add(nh)
                db.session.commit()
                regP=regP+1
            except Exception as inst:
                db.session.rollback()
                print(type(inst))    # the exception instance
                #print(inst)
                print("rasgo personalidad no se pudo crear.")
    print("registros guardados: "+str(regT)+" "+str(regB)+" "+str(regP))

if Perfil.get_count()==0:
    for i in range (300):
        lstHabilidades=[]

        lstHabilTecnica=Habilidad.get_by_tipo(Tipo_Habil.TECNICA)
        num_habilTecnica=Habilidad.get_count_by_tipo(Tipo_Habil.TECNICA)
        max_habilTecnica=math.trunc(num_habilTecnica*15/100)
        num_habilTecnicaAsignar = random.randint(1, max_habilTecnica)
        #print(num_habilTecnica," ",max_habilTecnica," ",num_habilTecnicaAsignar)
        for i in range(num_habilTecnicaAsignar):
            num_reg=random.randint(1, num_habilTecnica)
            id_habil=queHabil(lstHabilTecnica, num_reg)
            #print(num_reg," ",id_habil)
            if id_habil not in lstHabilidades:
                lstHabilidades.append(id_habil) 
            #print(lstHabilidades)

        lstHabilBlan=Habilidad.get_by_tipo(Tipo_Habil.BLANDA)
        num_habilBlanda = Habilidad.get_count_by_tipo(Tipo_Habil.BLANDA)
        max_habilBlanda=math.trunc(num_habilBlanda*20/100)
        num_habilBlandaAsignar = random.randint(1, max_habilBlanda)
        #print(num_habilBlanda," ",max_habilBlanda," ",num_habilBlandaAsignar)
        for i in range(num_habilBlandaAsignar):
            num_reg=random.randint(1, num_habilBlanda)
            id_habil=queHabil(lstHabilBlan, num_reg)
            #print(num_reg," ",id_habil)
            if id_habil not in lstHabilidades:
                lstHabilidades.append(id_habil) 
            #print(lstHabilidades)

        lstHabilPers=Habilidad.get_by_tipo(Tipo_Habil.PERSONALIDAD)
        num_habilPers=Habilidad.get_count_by_tipo(Tipo_Habil.PERSONALIDAD)
        max_habilPers=math.trunc(num_habilPers*30/100)
        num_habilPersAsignar = random.randint(1, max_habilPers)
        #print(num_habilPers," ",max_habilPers," ",num_habilPersAsignar)
        for i in range(num_habilPersAsignar):
            num_reg=random.randint(1, num_habilPers)
            id_habil=queHabil(lstHabilPers, num_reg)
            #print(num_reg," ",id_habil)
            if id_habil not in lstHabilidades:
                lstHabilidades.append(id_habil) 
            #print(lstHabilidades)

        long_lista=len(lstHabilidades)
        print(lstHabilidades)
        conteo=(func.count(HabilPerfil.id_perfil)).label('conteo')
        queryCumplenHabils=db.session.query(HabilPerfil.id_perfil, conteo).filter(HabilPerfil.id_habil.in_(lstHabilidades)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all()
        if len(queryCumplenHabils)==0:
            print("Adicionar1")
            adicionarPerfil(lstHabilidades)
        else:
            queryLongCorrecta=db.session.query(HabilPerfil.id_perfil, conteo).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all()    
            existe=False
            for h in queryCumplenHabils:
                for hh in queryLongCorrecta:
                    if h.id_perfil==hh.id_perfil:
                        existe=True
                        break
                if existe==True:
                    break
            if not existe:
                print("Adicionar2")
                adicionarPerfil(lstHabilidades)





"""lstHabils=[1,10,20]
long_lista=len(lstHabils)
conteo=(func.count(HabilPerfil.id_perfil)).label('conteo')
queryCumplenHabils=db.session.query(HabilPerfil.id_perfil).filter(HabilPerfil.id_habil.in_(lstHabils)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all()
for h in queryCumplenHabils:
    print(h)
queryCumplenHabil2=db.session.query(HabilPerfil.id_perfil, conteo).filter(HabilPerfil.id_habil.in_(lstHabils)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all()
for h in queryCumplenHabil2:
    print(h)
print(len(queryCumplenHabils),"",len(queryCumplenHabil2))

subquery=db.session.query(HabilPerfil.id_perfil).filter(HabilPerfil.id_habil.in_(lstHabils)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).subquery()
lstCumplenHabils = db.session.query(HabilPerfil.id_perfil, HabilPerfil.id_habil, HabilPerfil.valoracion).filter(HabilPerfil.id_perfil.in_(db.session.query(HabilPerfil.id_perfil).filter(HabilPerfil.id_habil.in_(lstHabils)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista)))
print(lstCumplenHabils.count())
for h in lstCumplenHabils:
    print(h)"""










        #for h in db.session.query(HabilPerfil.id_perfil, conteo).filter(HabilPerfil.id_habil.in_(lstHabilidades)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all():
        #    print(h.id_perfil," ", h.conteo)
        #for h in db.session.query(HabilPerfil.id_perfil, conteo).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all():
        #    print(h.id_perfil," ",h.conteo)

        #subquery=db.session.query(HabilPerfil.id_perfil, conteo).filter(HabilPerfil.id_habil.in_(lstHabilidades)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).subquery()
        #if db.session.query(HabilPerfil.id_perfil, conteo).filter(HabilPerfil.id_habil.in_(lstHabilidades)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).count()==0:
        #    print("Adicionar")
        #    adicionarPerfil(lstHabilidades)
        #else:
        #    print("QUERY")
        #    query=db.session.query(HabilPerfil.id_perfil, conteo).filter(HabilPerfil.id_habil.in_(lstHabilidades)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all()
        #    for hp in query:
        #        print(hp.id_perfil)
            #query = db.session.query(HabilPerfil.id_perfil, conteo).filter(HabilPerfil.id_perfil.in_(subquery)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all()
            #if db.session.query(HabilPerfil.id_perfil, conteo).filter(HabilPerfil.id_perfil.in_(subquery)).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all().count()==0:
            #    print("Adicionar")
            #    adicionarPerfil(lstHabilidades)

        #HPconN = aliased(HabilPerfil)
        #HP = aliased(HabilPerfil)
        #conteo=(func.count(HabilPerfil.id_perfil)).label('conteo')
        #for h in db.session.query(HabilPerfil.id_perfil, conteo).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all():
        #    print(h.id_perfil," ",conteo)

        #qHP=db.session.query(HabilPerfil.id_perfil, conteo).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).all()
        #db.session.query(qHP.id_perfil, HP.id_habil).filter(qHP.id_perfil==HP.id_perfil).all()

        #for h in db.session.query(HabilPerfil.id_perfil, conteo).group_by(HabilPerfil.id_perfil).having(conteo==long_lista).join(HP, HabilPerfil.id_perfil==HP.id_perfil).all():
        #    print(h.id_perfil," ",h.id_habil, end="")

#query = session.query(Residents).filter(Residents.apartment_id.in_(subquery))
#lst=[1,2,3]
#for h in Habilidad.query.filter(Habilidad.id.in_(lst)):
#    print(h.nombre)

#from sqlalchemy import func session.query(Table.column, func.count(Table.column)).group_by(Table.column).all()

#subquery = session.query(Apartments.id).filter(Apartments.postcode==2000).subquery()

#long_lista=1
#conteo=(func.count(Habilidad.id)).label('conteo')
#for h in db.session.query(Habilidad.id, conteo).filter(Habilidad.id.in_(lst)).group_by(Habilidad.id).having(conteo==long_lista).all():
#    print(h.id)


#subquery=db.session.query(Habilidad.id, conteo).filter(Habilidad.id.in_(lst)).group_by(Habilidad.id).having(conteo==long_lista).all().subquery()
#query = db.session.query(Habilidad.id).filter(Habilidad.id.in_(subquery))
#for h in Habilidad.query.filter(Habilidad.id.in_(lst)).group_by(id).all():
#    print(h.id)

