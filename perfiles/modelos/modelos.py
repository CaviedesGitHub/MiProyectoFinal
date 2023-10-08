import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import DateTime, Date
from sqlalchemy.sql import func

db = SQLAlchemy()

class Nivel_Habil(enum.Enum):
    ALTO = 1
    MEDIO = 2
    BAJO = 3

class Tipo_Habil(enum.Enum):
    TECNICA = 1
    BLANDA = 2
    PERSONALIDAD = 3

class Perfil(db.Model):
    __tablename__ = 'perfil'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, *args, **kw):
        super(Perfil, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Perfil.query.get(id)

    @staticmethod
    def get_count():
        return Perfil.query.count()
    
    @staticmethod
    def get_perfil(id_perfil):
        return Perfil.query.count()

class PerfilSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Perfil
        include_relationships = True
        load_instance = True

perfil_schema = PerfilSchema()

class HabilPerfil(db.Model):
    __tablename__ = 'habilperfil'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_perfil = db.Column(db.Integer, nullable=False)
    id_habil = db.Column(db.Integer, nullable=False)
    valoracion = db.Column(db.Enum(Nivel_Habil), nullable=False, default=Nivel_Habil.BAJO)  

    def __init__(self, *args, **kw):
        super(HabilPerfil, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return HabilPerfil.query.get(id)

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        else:
            return value.name #{'llave':value.name, 'valor':value.value} #{value.name}  #{'llave':value.name, 'valor':value.value}

class HabilPerfilSchema(SQLAlchemyAutoSchema):
    valoracion=EnumADiccionario(attribute=('valoracion'))
    class Meta:
        model = HabilPerfil
        include_relationships = True
        load_instance = True

habilperfil_schema = HabilPerfilSchema()



class Habilidad(db.Model):
    __tablename__ = 'habilidad'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    tipo = db.Column(db.Enum(Tipo_Habil), nullable=False, default=Tipo_Habil.PERSONALIDAD)  

    def __init__(self, *args, **kw):
        super(Habilidad, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Habilidad.query.get(id)

    @staticmethod
    def get_count():
        return Habilidad.query.count()

    @staticmethod
    def get_by_tipo(tipo):
        return Habilidad.query.filter_by(tipo=tipo)

    @staticmethod
    def get_count_by_tipo(tipo):
        return Habilidad.query.filter_by(tipo=tipo).count()

class HabilidadSchema(SQLAlchemyAutoSchema):
    tipo=EnumADiccionario(attribute=('tipo'))
    class Meta:
        model = Habilidad
        include_relationships = True
        load_instance = True

habilidad_schema = HabilidadSchema()

