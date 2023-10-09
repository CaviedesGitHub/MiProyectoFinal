import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime, Date
from sqlalchemy.sql import func

db = SQLAlchemy()

class Estado(enum.Enum):
    ACTIVO = 1
    INACTIVO = 2

class Nivel_Estudios(enum.Enum):
    PREGRADO = 1
    ESPECIALIZACION = 2
    MAESTRIA = 3
    DOCTORADO = 4
    DIPLOMADOS = 5
    CURSOS = 6

class Candidato(db.Model):
    __tablename__ = 'candidato'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    apellidos = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    documento = db.Column(db.Integer, nullable=False, unique=True)
    fecha_nac = db.Column(Date(), nullable=True)
    email = db.Column(db.Unicode(128), nullable=False, unique=True)
    phone = db.Column(db.Unicode(128))
    ciudad = db.Column(db.Unicode(128))
    direccion = db.Column(db.Unicode(128))
    num_perfil = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True)
    estado = db.Column(db.Enum(Estado), nullable=False, default=Estado.ACTIVO)  

    def __init__(self, *args, **kw):
        super(Candidato, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Candidato.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Candidato.query.filter_by(email=email).first()

    @staticmethod
    def get_count():
        return Candidato.query.count()

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        else:
            return value.name #{'llave':value.name, 'valor':value.value} #{value.name}  #{'llave':value.name, 'valor':value.value}
    
class CandidatoSchema(SQLAlchemyAutoSchema):
    estado=EnumADiccionario(attribute=('estado'))
    class Meta:
        model = Candidato
        include_relationships = True
        load_instance = True

candidato_schema = CandidatoSchema()


class Datos_Laborales(db.Model):
    __tablename__ = 'datos_laborales'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_cand = db.Column(db.Integer, nullable=False)

    empresa = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    cargo = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    funciones = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    fecha_ing = db.Column(Date(), nullable=True)
    fecha_sal = db.Column(Date(), nullable=True)

    def __init__(self, *args, **kw):
        super(Datos_Laborales, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Datos_Laborales.query.get(id)

 
class Datos_LaboralesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Datos_Laborales
        include_relationships = True
        load_instance = True

datos_laborales_schema = Datos_LaboralesSchema()



class Datos_Academicos(db.Model):
    __tablename__ = 'datos_academicos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_cand = db.Column(db.Integer, nullable=False)
    institucion = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    titulo = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    anio = db.Column(db.Integer, nullable=False, default=2023)
    nivel = db.Column(db.Enum(Nivel_Estudios), nullable=False, default=Nivel_Estudios.CURSOS)  

    def __init__(self, *args, **kw):
        super(Datos_Academicos, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Datos_Academicos.query.get(id)

    @staticmethod
    def get_count():
        return Datos_Academicos.query.count()

    
class Datos_AcademicosSchema(SQLAlchemyAutoSchema):
    nivel=EnumADiccionario(attribute=('nivel'))
    class Meta:
        model = Datos_Academicos
        include_relationships = True
        load_instance = True

datos_academicos_schema = Datos_AcademicosSchema()