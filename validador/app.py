from validador import create_app
from validador.vistas.vistas import VistaPing, VistaPerfil
from flask_restful import Api
from flask_jwt_extended import JWTManager

app=create_app('default')
app_context=app.app_context()
app_context.push()

#db.init_app(app)
#db.create_all()


api = Api(app)
api.add_resource(VistaPerfil, '/validador/perfiles')
api.add_resource(VistaPing, '/validador/ping')


jwt = JWTManager(app)