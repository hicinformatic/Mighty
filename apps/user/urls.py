from mighty.apps.user.views import UserViewSet
from django.urls import path, include

urlpatterns = [path('user/', include(UserViewSet().urls)),]