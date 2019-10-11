from mighty.apps.nationality.views import NationalityViewSet
from django.urls import path, include

urlpatterns = [path('nationality/', include(NationalityViewSet().urls)),]