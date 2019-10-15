from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.module_loading import import_string
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from django.urls import reverse, NoReverseMatch

from mighty.functions import encrypt, decrypt
from mighty.apps.authenticate import send_sms, send_email, _
from mighty.apps.authenticate.apps import AuthenticateConfig

from urllib.parse import quote_plus, unquote_plus
UserModel = get_user_model()


methods = [method for method in AuthenticateConfig.methods if hasattr(AuthenticateConfig.method, method) and getattr(AuthenticateConfig.method, method)]
methods_ws = method = [method for method in AuthenticateConfig.methods_ws if hasattr(AuthenticateConfig.method, method) and getattr(AuthenticateConfig.method, method)]


class UserSearchForm(forms.Form):
    search = forms.CharField(label=_.f_search)
    method = forms.CharField(widget=forms.HiddenInput)
    user_cache = None
    method_cache = None
    success_url = None
    error_messages = {
        'invalid_search': _.e_invalid_search,
        'invalid_method': _.e_invalid_method,
        'inactive': _.e_inactive,
        'cant_send': _.e_cant_send,
        'method_not_allowed': _.e_method_not_allowed,
    }

    def clean(self):
        search = self.cleaned_data.get('search')
        method = self.cleaned_data.get("method")
    
        try:
            self.user_cache = UserModel.objects.get(Q(username=search) | Q(email=search) | Q(phone=search))
            self.confirm_login_allowed(self.user_cache)
            self.method_cache = self.cleaned_data.get('method')
            self.user_cache.add_code()
            if self.method_cache not in methods:
                raise forms.ValidationError(self.error_messages['method_not_allowed'], code='method_not_allowed',)
            if self.method_cache in methods_ws:
                if self.method_cache == 'sms' and self.user_cache.phone is None:
                    raise forms.ValidationError(self.error_messages['cant_send'], code='cant_send',)
                if self.method_cache == 'email' and self.user_cache.email is None:
                    raise forms.ValidationError(self.error_messages['cant_send'], code='cant_send',)
                status = send_sms(self.user_cache) if self.method_cache == 'sms' else send_email(self.user_cache)
                if not status:
                    raise forms.ValidationError(self.error_messages['cant_send'], code='cant_send',)
        except UserModel.DoesNotExist:
            raise forms.ValidationError(self.error_messages['invalid_search'], code='invalid_search',)

        try:
            useruidandmethod = '%s:%s' % (method, str(self.user_cache.uid))
            useruidandmethod = encrypt(settings.SECRET_KEY[:16], useruidandmethod).decode('utf-8')
            self.success_url = reverse('mighty:%s-login' % method, kwargs={'uid': quote_plus(useruidandmethod)})
        except NoReverseMatch:
            raise forms.ValidationError(self.error_messages['invalid_method'], code='invalid_method',)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
            if not user.is_active:
                raise forms.ValidationError(self.error_messages['inactive'], code='inactive', )
            
class AuthenticateTwoFactorForm(AuthenticationForm):
    def __init__(self, uid, method, *args, **kwargs): 
        super(AuthenticateTwoFactorForm, self).__init__(*args, **kwargs) 
        self.uid = uid
        self.method = method
        self.fields.pop('username')

    def clean(self):
        password = self.cleaned_data.get('password')
        if password:
            self.user_cache = authenticate(self.request, username=self.uid, password=password, **{'method': self.method})
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data