
from django.urls import path, include
from mighty.apps.authenticate.views import EmailViewSet, SmsViewSet
from mighty.apps.authenticate.views.authenticate import Login, LoginBasic


urlpatterns = [
    path('email/', include(EmailViewSet().urls)),
    path('sms/', include(SmsViewSet().urls)),
    path('login/', include([
        path("basic/<uid>", LoginBasic.as_view(), name="basic-login"),
        path("", Login.as_view(), name="login-login"),
    ])),
]