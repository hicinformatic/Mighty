from django.conf import settings
from django.urls import path, include

from mighty.apps.user.views import UserViewSet
urlpatterns = [path('user/', include(UserViewSet().urls)),]

if 'rest_framework' in settings.INSTALLED_APPS:
    from mighty.apps.user.views import UserApiViewSet
    urlpatterns += [path('api/user/', include(UserApiViewSet().urls)),]