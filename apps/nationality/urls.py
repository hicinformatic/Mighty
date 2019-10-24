from django.conf import settings
from django.urls import path, include

from mighty.apps.nationality.views import NationalityViewSet
urlpatterns = [path('nationality/', include(NationalityViewSet().urls)),]


if 'rest_framework' in settings.INSTALLED_APPS:
    #from rest_framework.routers import SimpleRouter
    from mighty.apps.nationality.views import NationalityApiViewSet
    urlpatterns += [path('api/nationality/', include(NationalityApiViewSet().urls)),]
    #router = SimpleRouter()
    #router.register('nationality', NationalityApiViewSet)
    #apipatterns = router.urls