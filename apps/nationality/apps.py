from django.apps import AppConfig

import os.path

class Config:
    directory = os.path.dirname(os.path.realpath(__file__))

class NationalityConfig(AppConfig, Config):
    name = 'nationality'
