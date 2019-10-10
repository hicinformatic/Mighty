from mighty.views import DetailView, AdminView, FormView
from mighty.models.authenticate import Email, Sms

class CheckStatus(DetailView):
    template_name = 'authenticate/check.html'
    model = Email

    def get_context_data(self, **kwargs):
        context = super(CheckStatus, self).get_context_data(**kwargs)
        status = self.object.check_status()
        context.update({'status': status})
        return context

class AdminCheckStatus(CheckStatus, AdminView):
    template_name = 'authenticate/admin/check.html'

from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth import get_user_model
from mighty.apps.authenticate.forms import UserSearchForm, AuthenticateTwoFactorForm

UserModel = get_user_model()
class Login(FormView):
    model = UserModel
    form_class = UserSearchForm
    template_name = 'authenticate/login.html'
    user = None
    method = None

    def form_valid(self, form):
        self.user = form.user_cache
        self.method = form.method_cache
        return super(Login, self).form_valid(form)

    def get_success_url(self):
        return reverse('mighty:login-%s' % self.method, kwargs={'uid': self.user.uid})

class LoginView(LoginView):
    form_class = AuthenticateTwoFactorForm

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs.update({'request' : self.request, 'uid': self.kwargs.get('uid')})
        return kwargs 