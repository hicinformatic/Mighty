from django.apps import AppConfig
from django.conf import settings

import os

class Config:
    methods = ['email', 'sms', 'basic']
    methods_ws = ['email', 'sms']

    class method:
        email = True
        sms = True
        basic = True

class AuthenticateConfig(AppConfig, Config):
    name = 'authenticate'

    