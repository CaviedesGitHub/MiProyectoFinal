from motoremp import create_app
from motoremp.vistas.vistas import VistaPing, VistaEmparejar
from flask_restful import Api
from flask_jwt_extended import JWTManager

app=create_app('default')
app_context=app.app_context()
app_context.push()

#db.init_app(app)
#db.create_all()

api = Api(app)
api.add_resource(VistaEmparejar, '/motor/emparejar')
api.add_resource(VistaPing, '/motor/ping')


jwt = JWTManager(app)