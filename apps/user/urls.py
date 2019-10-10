from mighty.models.user import Nationality, User
from mighty.apps.user.views import NationalityViewSet, UserViewSet
from django.urls import path, include

urlpatterns = [
    path('user/', include(UserViewSet().urls)),
    path('nationality/', NationalityViewSet().view('list').as_view()),
]