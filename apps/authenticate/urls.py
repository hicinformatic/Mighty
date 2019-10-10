
from django.urls import path, include
from mighty.apps.authenticate.views import EmailViewSet, SmsViewSet

urlpatterns = [
    path('email/', include(EmailViewSet().urls)),
    path('sms/', include(SmsViewSet().urls)),
]