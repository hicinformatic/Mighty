
from django.urls import path, include
from mighty.apps.authenticate.views import EmailViewSet, SmsViewSet
from mighty.apps.authenticate.views.authenticate import Logout, Login, LoginBasic, LoginSms, LoginEmail
from mighty.apps.authenticate.apps import AuthenticateConfig




loginviews = []
if AuthenticateConfig.method.basic:
    loginviews.append(path("basic/<uid>", LoginBasic.as_view(), name="login-basic"))
if AuthenticateConfig.method.email:
    loginviews.append(path("email/<uid>", LoginEmail.as_view(), name="login-email"))
if AuthenticateConfig.method.sms:    
    loginviews.append(path("sms/<uid>", LoginSms.as_view(), name="login-sms"))
loginviews.append(path("", Login.as_view(), name="login-auth"))

urlpatterns = [
    path('email/', include(EmailViewSet().urls)),
    path('sms/', include(SmsViewSet().urls)),
    path("logout/", Logout.as_view(), name="logout"),
    path('login/', include(loginviews)),
]