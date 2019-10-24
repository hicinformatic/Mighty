from django.conf import settings
from django.urls import path, include

from mighty.apps.user.views import UserViewSet
urlpatterns = [path('user/', include(UserViewSet().urls)),]

#if 'rest_framework' in settings.INSTALLED_APPS:
#    from rest_framework.routers import SimpleRouter
#    from mighty.apps.user.views import UserApiViewSet
#    router = SimpleRouter()
#    router.register('user', UserApiViewSet, basename='user-api')
#    apipatterns = router.urls