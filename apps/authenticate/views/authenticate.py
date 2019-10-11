from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from mighty.functions import encrypt, decrypt
from mighty.apps.authenticate.forms import UserSearchForm, AuthenticateTwoFactorForm
from mighty.views import DetailView, AdminView, FormView, BaseView
from mighty.models.authenticate import Email, Sms
from mighty.apps.authenticate import _

from urllib.parse import quote_plus, unquote_plus

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

    def get_header(self):
        return {
            'title': _.t_authenticate
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "send_method": _.send_method,
            "method_sms": _.method_sms,
            "method_email": _.method_email,
        })
        return context

    def get_success_url(self):
        useruid = encrypt(settings.SECRET_KEY[:16], str(self.user.uid)).decode('utf-8')
        return reverse('mighty:%s-login' % self.method, kwargs={'uid': quote_plus(useruid)})

class LoginView(BaseView, LoginView):
    form_class = AuthenticateTwoFactorForm

    def get_header(self):
        return {
            'title': _.t_authenticate
        }

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        useruid = decrypt(settings.SECRET_KEY[:16], unquote_plus(self.kwargs.get('uid'))).decode("utf-8")
        kwargs.update({'request' : self.request, 'uid': useruid})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"submit": _.submit_code})
        return context

class LoginEmail(LoginView):
    template_name = 'authenticate/login/email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"howto": _.tpl_email_code})
        return context

class LoginSms(LoginView):
    template_name = 'authenticate/login/sms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"howto": _.tpl_sms_code})
        return context