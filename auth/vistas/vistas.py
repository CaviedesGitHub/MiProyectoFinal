from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from auth.modelos.modelos import db, Usuario, UsuarioSchema, UserType


usuario_schema = UsuarioSchema()

class VistaSignIn(Resource):   
    def post(self):
        tipo = request.json.get('tipo', None)
        pass1 = request.json.get('password', None)
        pass2 = request.json.get('password2', None)
        nombre = request.json.get('nombre', None)
        if tipo is not None and pass1 is not None and pass2 is not None and nombre is not None:
            if UserType.EMPRESA.name==tipo or UserType.CANDIDATO.name==tipo or UserType.CANDIDATO.name==tipo:
                if pass1==pass2:
                    usuario=Usuario.query.filter(Usuario.nombre == nombre).first()
                    if usuario is None:
                        nuevo_usuario = Usuario(nombre=nombre, tipo=UserType[tipo])
                        nuevo_usuario.set_password(pass1)
                        db.session.add(nuevo_usuario)
                        db.session.commit()
                        additional_claims = {"aud": nuevo_usuario.tipo.name, "MyUserType": "EMPRESA"}
                        token_de_acceso = create_access_token(identity=nuevo_usuario.id, additional_claims=additional_claims)
                        return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id}
                    else:
                        return {"mensaje": "Usuario Ya Existe"}
                else:
                    return {"mensaje": "No coincide password de confirmación"}
            else:
                return {"mensaje": "Valor Invalido para Tipo de Usuario"}
        else:
            return {"mensaje": "Faltan algunos datos necesarios"}

class VistaLogIn(Resource):
    def post(self):
        pass1 = request.json.get('password', None)
        nombre = request.json.get('nombre', None)
        if nombre is not None and pass1 is not None:
            usuario = Usuario.query.filter(Usuario.nombre == nombre).first()
            db.session.commit()
            if usuario is not None and usuario.authenticate(pass1):
                additional_claims = {"aud": usuario.tipo.name, "MyUserType": "EMPRESA"}
                token_de_acceso = create_access_token(identity=usuario.id, additional_claims=additional_claims)
                return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}
            else:
                return {"mensaje":"LogIn Incorrecto."}, 404
        else:
            return {"mensaje": "Faltan datos necesarios"}
        
class VistaUsuario(Resource):   
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return usuario_schema.dump(usuario)

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        if request.json.get("password", None) is not None:
           usuario.set_password(request.json["password"])
        usuario.nombre=request.json.get("nombre", usuario.nombre)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return "Usuario Borrado.",  204

class VistaPing(Resource):
    def get(self):
        print("pong")
        return {"Mensaje":"Pong"}, 200


