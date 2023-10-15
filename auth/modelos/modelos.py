import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime, Date
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class UserType(enum.Enum):
    EMPRESA = 1
    CANDIDATO = 2
    EMPLEADO_ABC = 3

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING', unique=True)
    password = db.Column(db.Unicode(256))
    tipo = db.Column(db.Enum(UserType), nullable=False)  

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def __init__(self, *args, **kw):
        super(Usuario, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def get_by_nombre(nombre):
        return Usuario.query.filter_by(nombre=nombre).first()

    @staticmethod
    def get_count():
        return Usuario.query.count()

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        else:
            return value.name #{'llave':value.name, 'valor':value.value} #{value.name}  #{'llave':value.name, 'valor':value.value}
    
class UsuarioSchema(SQLAlchemyAutoSchema):
    tipo=EnumADiccionario(attribute=('tipo'))
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

usuario_schema = UsuarioSchema()

