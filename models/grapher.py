from django.db import models
from django.conf import settings
from mighty.apps.grapher.models import Template, Graph


class Template(Template):
    pass

class Graph(Graph):
    templates = models.ManyToManyField(Template)