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

class Empresa(db.Model):
    __tablename__ = 'empresas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING', unique=True)
    tipo = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    correo = db.Column(db.Unicode(128), nullable=False, unique=True)
    celular = db.Column(db.Unicode(128), nullable=True)
    contacto = db.Column(db.Unicode(128), default='MISSING')
    pais = db.Column(db.Unicode(128))
    ciudad = db.Column(db.Unicode(128))
    direccion = db.Column(db.Unicode(128))
    id_usuario = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True)
    estado = db.Column(db.Enum(Estado), nullable=False, default=Estado.ACTIVO)  

    def __init__(self, *args, **kw):
        super(Empresa, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Empresa.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Empresa.query.filter_by(email=email).first()

    @staticmethod
    def get_count():
        return Empresa.query.count()

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        else:
            return value.name #{'llave':value.name, 'valor':value.value} #{value.name}  #{'llave':value.name, 'valor':value.value}
    
class EmpresaSchema(SQLAlchemyAutoSchema):
    estado=EnumADiccionario(attribute=('estado'))
    class Meta:
        model = Empresa
        include_relationships = True
        load_instance = True

empresa_schema = EmpresaSchema()


class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_emp = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    descripcion = db.Column(db.Unicode(128), nullable=False, default='MISSING')


    def __init__(self, *args, **kw):
        super(Proyecto, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Proyecto.query.get(id)

    @staticmethod
    def get_by_empresa(id_emp):
        return Proyecto.query.filter(Proyecto.id_emp==id_emp).all()

 
class ProyectoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Proyecto
        include_relationships = True
        load_instance = True

proyecto_schema = ProyectoSchema()


class PerfilesProyecto(db.Model):
    __tablename__ = 'perfiles_proyectos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    id_proy = db.Column(db.Integer, nullable=False)
    id_perfil = db.Column(db.Integer, nullable=False)
    id_cand = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, *args, **kw):
        super(PerfilesProyecto, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return PerfilesProyecto.query.get(id)

    @staticmethod
    def get_count():
        return PerfilesProyecto.query.count()

    
class PerfilesProyectoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PerfilesProyecto
        include_relationships = True
        load_instance = True

perfiles_proyecto_schema = PerfilesProyectoSchema()


class EmpleadoEmpresa(db.Model):
    __tablename__ = 'empleado_empresa'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_emp = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.Unicode(128), nullable=False, default='MISSING')
    id_perfil = db.Column(db.Integer, nullable=True)


    def __init__(self, *args, **kw):
        super(EmpleadoEmpresa, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return EmpleadoEmpresa.query.get(id)

 
class EmpleadoEmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmpleadoEmpresa
        include_relationships = True
        load_instance = True

empleado_empresa_schema = EmpleadoEmpresaSchema()


class Encargado(db.Model):
    __tablename__ = 'encargado'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_proy = db.Column(db.Integer, nullable=False)
    id_empleado = db.Column(db.Integer, nullable=False)
    rol = db.Column(db.Unicode(128), nullable=False, default='MISSING')


    def __init__(self, *args, **kw):
        super(Encargado, self).__init__(*args, **kw)

    def get_id(self):
        return self.id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Encargado.query.get(id)

 
class EncargadoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Encargado
        include_relationships = True
        load_instance = True

encargado_schema = EncargadoSchema()
