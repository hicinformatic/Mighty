from django.apps import AppConfig
from django.conf import settings

import os

class Config:
    class Field:
        username = 'email'
        required = ('username',)

class UserConfig(AppConfig, Config):
    name = 'mighty.app.user'

    def ready(self):
        from . import signals