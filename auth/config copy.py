# Fichero de configuración config.py

class Config(object):
    SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'proyecto2_2023'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@abcjobs.chpn4nrvpnvk.us-east-1.rds.amazonaws.com:5432/CandidatoBD"
    JWT_ACCESS_TOKEN_EXPIRES = False

    HOST_PORT_GATEWAY = "http://localhost:5000"
    HOST_PORT_MOTOREMP1 = "http://localhost:5001"
    HOST_PORT_MOTOREMP2 = "http://localhost:5002"
    HOST_PORT_MOTOREMP3 = "http://localhost:5003"
    HOST_PORT_PERFILES = "http://localhost:5004"
    HOST_PORT_VALIDADOR = "http://localhost:5005"
    HOST_PORT_EMPRESA = "http://localhost:5006"
    HOST_PORT_AUTH = "http://localhost:5007"
    HOST_PORT_CANDIDATO = "http://candidato-env.eba-ppp3p2tu.us-east-2.elasticbeanstalk.com"
    HOST_PORT_PRUEBASTEC = "http://localhost:5009"



class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin@localhost:5432/CandidatosBD'
    JWT_ACCESS_TOKEN_EXPIRES = False

    HOST_PORT_GATEWAY = "http://localhost:5000"
    HOST_PORT_MOTOREMP1 = "http://localhost:5001"
    HOST_PORT_MOTOREMP2 = "http://localhost:5002"
    HOST_PORT_MOTOREMP3 = "http://localhost:5003"
    HOST_PORT_PERFILES = "http://localhost:5004"
    HOST_PORT_VALIDADOR = "http://localhost:5005"
    HOST_PORT_EMPRESA = "http://localhost:5006"
    HOST_PORT_AUTH = "http://localhost:5007"
    HOST_PORT_CANDIDATO = "http://localhost:5008"
    HOST_PORT_PRUEBASTEC = "http://localhost:5009"

class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin@localhost:5432/CandidatosBD'
    JWT_ACCESS_TOKEN_EXPIRES = False

    HOST_PORT_GATEWAY = "http://localhost:5000"
    HOST_PORT_MOTOREMP1 = "http://localhost:5001"
    HOST_PORT_MOTOREMP2 = "http://localhost:5002"
    HOST_PORT_MOTOREMP3 = "http://localhost:5003"
    HOST_PORT_PERFILES = "http://localhost:5004"
    HOST_PORT_VALIDADOR = "http://localhost:5005"
    HOST_PORT_EMPRESA = "http://localhost:5006"
    HOST_PORT_AUTH = "http://localhost:5007"
    HOST_PORT_CANDIDATO = "http://localhost:5008"
    HOST_PORT_PRUEBASTEC = "http://localhost:5009"

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin@localhost:5432/CandidatosBD'
    JWT_ACCESS_TOKEN_EXPIRES = False

    HOST_PORT_GATEWAY = "http://localhost:5000"
    HOST_PORT_MOTOREMP1 = "http://localhost:5001"
    HOST_PORT_MOTOREMP2 = "http://localhost:5002"
    HOST_PORT_MOTOREMP3 = "http://localhost:5003"
    HOST_PORT_PERFILES = "http://localhost:5004"
    HOST_PORT_VALIDADOR = "http://localhost:5005"
    HOST_PORT_EMPRESA = "http://localhost:5006"
    HOST_PORT_AUTH = "http://localhost:5007"
    HOST_PORT_CANDIDATO = "http://localhost:5008"
    HOST_PORT_PRUEBASTEC = "http://localhost:5009"