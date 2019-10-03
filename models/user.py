from django.db import models
from django.conf import settings
from mighty.apps.user.models import Nationality, User as FirstUser

class Nationality(Nationality):
    pass

class User(FirstUser):
    nationalities = models.ManyToManyField(Nationality, blank=True)

if 'mighty.apps.extend' in settings.INSTALLED_APPS:
    from mighty.models.extend import Extend, History
    from mighty.apps.extend.functions import related_name
    
    class UserExtend(Extend):
        parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name(User, 'extend'))

    class UserHistory(History):
        parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name(User, 'history'))


    class NationalityExtend(Extend):
        parent = models.ForeignKey(Nationality, on_delete=models.CASCADE, related_name=related_name(Nationality, 'extend'))

    class NationalityHistory(History):
        parent = models.ForeignKey(Nationality, on_delete=models.CASCADE, related_name=related_name(Nationality, 'history'))