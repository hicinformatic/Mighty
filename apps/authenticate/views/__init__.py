from mighty.views import ModelViewSet
from mighty.models.authenticate import Email, Sms

class EmailViewSet(ModelViewSet):
    slug = '<id:id>'
    model = Email

class SmsViewSet(ModelViewSet):
    model = Sms