from django.conf import settings
from django.urls import path, include

from mighty.apps.nationality.views import NationalityViewSet
urlpatterns = [path('nationality/', include(NationalityViewSet().urls)),]


if 'rest_framework' in settings.INSTALLED_APPS:
    from mighty.apps.nationality.views import NationalityApiViewSet
    urlpatterns += [path('api/nationality/', include(NationalityApiViewSet().urls)),]