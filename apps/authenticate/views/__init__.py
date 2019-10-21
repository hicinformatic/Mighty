from mighty.views import ModelViewSet
from mighty.apps.authenticate.views.authenticate import LoginEmail, LoginSms
from mighty.models.authenticate import Email, Sms

class EmailViewSet(ModelViewSet):
    slug = '<int:pk>'
    model = Email
    list_display = ('email', 'status',)

class SmsViewSet(ModelViewSet):
    slug = '<int:pk>'
    model = Sms
    list_display = ('phone', 'status',)