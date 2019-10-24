from django.conf import settings
from django.urls import path, include

from mighty.apps.grapher.views import GraphViewSet
urlpatterns = [path('grapher/', include(GraphViewSet().urls)),]


if 'rest_framework' in settings.INSTALLED_APPS:
    from mighty.apps.grapher.views import GraphApiViewSet
    urlpatterns += [path('api/grapher/', include(GraphApiViewSet().urls)),]
