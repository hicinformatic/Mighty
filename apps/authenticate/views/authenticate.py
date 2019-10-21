from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from mighty.functions import encrypt, decrypt
from mighty.apps.authenticate.forms import UserSearchForm, AuthenticateTwoFactorForm
from mighty.views import DetailView, AdminView, FormView, BaseView
from mighty.models.authenticate import Email, Sms
from mighty.apps.authenticate import _
from mighty.apps.authenticate.apps import AuthenticateConfig

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
    app_label = 'mighty'
    model_name = 'authenticate'
    form_class = UserSearchForm
    permission_required = ()
    user = None
    method = None

    def form_valid(self, form):
        self.user = form.user_cache
        self.method = form.method_cache
        self.success_url = form.success_url
        return super(Login, self).form_valid(form)

    def get_header(self):
        return {
            'title': _.t_authenticate
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "enable_email": AuthenticateConfig.method.email,
            "enable_sms": AuthenticateConfig.method.sms,
            "enable_basic": AuthenticateConfig.method.basic,
            "send_method": _.send_method,
            "send_basic": _.send_basic,
            "method_sms": _.method_sms,
            "method_email": _.method_email,
            "method_basic": _.method_basic,

        })
        return context

    def get_success_url(self):
        return self.success_url

class LoginView(BaseView, LoginView):
    app_label = 'mighty'
    model_name = 'authenticate'
    form_class = AuthenticateTwoFactorForm

    def get_header(self):
        return {'title': _.t_authenticate}

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        useruidandmethod = decrypt(settings.SECRET_KEY[:16], unquote_plus(self.kwargs.get('uid'))).decode("utf-8").split(':')
        kwargs.update({'request' : self.request, 'uid': useruidandmethod[1], 'method': useruidandmethod[0]})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"submit": _.submit_code})
        return context

class LoginEmail(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"howto": _.tpl_email_code})
        return context

class LoginSms(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"howto": _.tpl_sms_code})
        return context

class LoginBasic(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"howto": _.tpl_basic_code})
        return context