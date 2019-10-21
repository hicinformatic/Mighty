from django.apps import AppConfig
from django.conf import settings

import os

class Config:
    override = 'AUTHENTICATE'
    methods = ['email', 'sms', 'basic']
    methods_ws = ['email', 'sms']

    class method:
        email = True
        sms = True
        basic = True

if hasattr(settings, Config.override):
    for config,configs in getattr(settings, Config.override).items():
        if hasattr(Config, config):
            for key,value in configs.items():
                if hasattr(getattr(Config, config), key):
                    setattr(getattr(Config, config), key, value)

class AuthenticateConfig(AppConfig, Config):
    name = 'authenticate'

    