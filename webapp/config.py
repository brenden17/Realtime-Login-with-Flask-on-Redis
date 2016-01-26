import logging

class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    MONGODB_SETTING = {
    	'db': 'local',
    	'host': 'localhost',
    	'port': 27017
    }


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    MONGODB_SETTING = {
    	'db': 'local',
    	'host': 'localhost',
    	'port': 27017
    }
    LOGGING_FILE = 'application.log'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LEVEL = logging.DEBUG

