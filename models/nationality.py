from django.db import models
from django.conf import settings
from mighty.apps.nationality.models import Nationality

class Nationality(Nationality):
    pass

if 'mighty.apps.extend' in settings.INSTALLED_APPS:
    from mighty.models.extend import Extend, History
    from mighty.apps.extend.functions import related_name
    
    class NationalityExtend(Extend):
        parent = models.ForeignKey(Nationality, on_delete=models.CASCADE, related_name=related_name(Nationality, 'extend'))

    class NationalityHistory(History):
        parent = models.ForeignKey(Nationality, on_delete=models.CASCADE, related_name=related_name(Nationality, 'history'))