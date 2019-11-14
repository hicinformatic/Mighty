
from django.urls import path, include
from mighty.apps.authenticate.views import EmailViewSet, SmsViewSet
from mighty.apps.authenticate.views.authenticate import Logout, Login, LoginBasic, LoginSms, LoginEmail


urlpatterns = [
    path('email/', include(EmailViewSet().urls)),
    path('sms/', include(SmsViewSet().urls)),
    path("logout/", Logout.as_view(), name="logout"),
    path('login/', include([
        path("basic/<uid>", LoginBasic.as_view(), name="login-basic"),
        path("email/<uid>", LoginEmail.as_view(), name="login-email"),
        path("sms/<uid>", LoginSms.as_view(), name="login-sms"),
        path("", Login.as_view(), name="login-auth"),
    ])),
]