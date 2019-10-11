from mighty.views import ModelViewSet
from mighty.apps.authenticate.views.authenticate import LoginEmail, LoginSms
from mighty.models.authenticate import Email, Sms

class EmailViewSet(ModelViewSet):
    slug = '<int:pk>'
    model = Email
    list_display = ('email', 'status',)

    def __init__(self, model=None):
        super().__init__()
        self.addNotuseid('login')
        self.addView('login', LoginEmail, 'login/<uid>')

class SmsViewSet(ModelViewSet):
    slug = '<int:pk>'
    model = Sms
    list_display = ('phone', 'status',)

    def __init__(self, model=None):
        super().__init__()
        self.addNotuseid('login')
        self.addView('login', LoginSms, 'login/<uid>')