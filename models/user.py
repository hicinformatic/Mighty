from django.db import models
from django.conf import settings
from mighty.apps.user.models import User

if 'mighty.apps.nationality' in settings.INSTALLED_APPS:
    from mighty.models.nationality import Nationality
    class User(User):
        nationalities = models.ManyToManyField(Nationality, blank=True)
else:
    class User(User):
        pass

if 'mighty.apps.extend' in settings.INSTALLED_APPS:
    from mighty.models.extend import Extend, History
    from mighty.apps.extend.functions import related_name
    
    class UserExtend(Extend):
        parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name(User, 'extend'))

    class UserHistory(History):
        parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name=related_name(User, 'history'))