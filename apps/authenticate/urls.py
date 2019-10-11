
from django.urls import path, include
from mighty.apps.authenticate.views import EmailViewSet, SmsViewSet
from mighty.apps.authenticate.views.authenticate import Login


urlpatterns = [
    path('email/', include(EmailViewSet().urls)),
    path('sms/', include(SmsViewSet().urls)),
    path('login/', Login.as_view()),
]