from django.conf import settings
from django.db import connection, models

if connection.vendor == 'mysql': from django_mysql.models import JSONField
elif connection.vendor == 'postgresql': from django.contrib.postgres.fields import JSONField
else: from jsonfield import JSONField

class JSONField(JSONField):
    pass

if 'mighty.apps.user' in settings.INSTALLED_APPS:
    from mighty.models.user import User

if 'mighty.apps.permissions' in settings.INSTALLED_APPS:
    from mighty.models.permissions import PermissionAsk

if 'mighty.apps.authenticate' in settings.INSTALLED_APPS:
    from mighty.models.authenticate import Email, Sms

if 'mighty.apps.grapher' in settings.INSTALLED_APPS:
    from mighty.models.grapher import Graph

