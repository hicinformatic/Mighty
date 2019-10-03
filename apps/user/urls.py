from mighty.apps.user.views import UserViewSet
from django.urls import include, path

urlpatterns = [
    path('user/', include([
        path('', UserViewSet.ListView(), name='user-list'),
    ])),
]