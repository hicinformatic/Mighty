from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth import get_user_model

from mighty import views
from mighty.apps.authenticate import forms

UserModel = get_user_model()
class Login(views.FormView):
    model = UserModel
    form_class = forms.UserSearchForm
    template_name = 'authenticate/login.html'
    permission_required = ()
    user = None
    method = None

    def form_valid(self, form):
        self.user = form.user_cache
        self.method = form.method_cache
        return super(Login, self).form_valid(form)

    def get_success_url(self):
        return reverse('mighty:login-%s' % self.method, kwargs={'uid': self.user.uid})

class LoginView(LoginView):
    form_class = forms.AuthenticateTwoFactorForm
    permission_required = ()

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs.update({'request' : self.request, 'uid': self.kwargs.get('uid')})
        return kwargs 