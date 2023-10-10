import datetime
from flask import Flask
import os

def create_app(config_name, settings_module='gateway.config.DevelopmentConfig'):
    app=Flask(__name__)
    app.config.from_object(settings_module)
    return app
    