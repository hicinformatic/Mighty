from django.contrib import admin

from mighty.models import PermissionAsk
from mighty.apps.permissions.admin import PermissionAskAdmin

@admin.register(PermissionAsk)
class PermissionAskAdmin(PermissionAskAdmin):
    pass