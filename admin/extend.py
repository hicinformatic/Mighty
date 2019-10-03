from django.contrib import admin

from mighty.models.extend import Field
from mighty.apps.extend.admin import FieldAdmin

@admin.register(Field)
class FieldAdmin(FieldAdmin):
    pass