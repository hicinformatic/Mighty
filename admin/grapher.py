from django.contrib import admin
from django.conf import settings

from mighty.models import grapher as models
from mighty.apps.grapher.admin import GraphAdmin


@admin.register(models.Graph)
class GraphAdmin(GraphAdmin):
    pass