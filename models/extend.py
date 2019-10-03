from django.db import models
from mighty.apps.extend.models import Field, Extend, History

class Field(Field):
    pass

class Extend(Extend):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    class Meta(Extend.Meta):
        abstract = True

class History(History):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    class Meta(History.Meta):
        abstract = True