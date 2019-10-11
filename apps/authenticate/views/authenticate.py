from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth import get_user_model

from mighty.apps.authenticate.forms import UserSearchForm, AuthenticateTwoFactorForm
from mighty.views import DetailView, AdminView, FormView
from mighty.models.authenticate import Email, Sms

class CheckStatus(DetailView):
    template_name = 'authenticate/check.html'

    def get_context_data(self, **kwargs):
        context = super(CheckStatus, self).get_context_data(**kwargs)
        status = self.object.check_status()
        context.update({'status': status})
        return context

class AdminSmsCheckStatus(CheckStatus, AdminView):
    template_name = 'authenticate/admin/check.html'
    model = Sms
    permission_required = ('mighty:view_sms', 'mighty:check_sms')

class AdminEmailCheckStatus(CheckStatus, AdminView):
    template_name = 'authenticate/admin/check.html'
    model = Email
    permission_required = ('mighty:view_email', 'mighty:check_email')


from mighty.functions import encrypt, decrypt
from django.conf import settings
from urllib.parse import quote_plus, unquote_plus
UserModel = get_user_model()
class Login(FormView):
    model = UserModel
    form_class = UserSearchForm
    template_name = 'authenticate/login.html'
    permission_required = ()
    user = None
    method = None

    def form_valid(self, form):
        self.user = form.user_cache
        self.method = form.method_cache
        return super(Login, self).form_valid(form)

    def get_success_url(self):
        useruid = encrypt(settings.SECRET_KEY[:16], str(self.user.uid)).decode('utf-8')
        return reverse('mighty:%s-login' % self.method, kwargs={'uid': quote_plus(useruid)})

class LoginView(LoginView):
    form_class = AuthenticateTwoFactorForm

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        useruid = decrypt(settings.SECRET_KEY[:16], unquote_plus(self.kwargs.get('uid'))).decode("utf-8")
        kwargs.update({'request' : self.request, 'uid': useruid})
        return kwargs

class LoginEmail(LoginView):
    template_name = 'authenticate/login/email.html'

class LoginSms(LoginView):
    template_name = 'authenticate/login/sms.html'