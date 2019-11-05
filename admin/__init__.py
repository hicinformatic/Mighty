from django.contrib import admin
from django.contrib.auth.models import Permission
from django.conf import settings

from mighty.admin.site import AdminSite

mysite = AdminSite()
admin.site = mysite
admin.sites.site = mysite

if 'mighty.apps.extend' in settings.INSTALLED_APPS:
    from mighty.admin import extend

if 'mighty.apps.nationality' in settings.INSTALLED_APPS:
    from mighty.admin import nationality

if 'mighty.apps.user' in settings.INSTALLED_APPS:
    from mighty.admin import user

if 'mighty.apps.permissions' in settings.INSTALLED_APPS:
    from mighty.admin import permissions

if 'mighty.apps.authenticate' in settings.INSTALLED_APPS:
    from mighty.admin import authenticate

if 'mighty.apps.authenticate' in settings.INSTALLED_APPS:
    from mighty.admin import grapher
