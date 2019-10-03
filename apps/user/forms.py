from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from mighty.apps.user.apps import UserConfig as conf

class UserCreationForm(UserCreationForm):
    class UsernameField(UsernameField):
        pass

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in conf.Field.required + (conf.Field.username,):
            try:
                self.fields[field] = getattr(forms, "%sField" % field.title())(required=True)
            except AttributeError:
                self.fields[field] = getattr(self, "%sField" % field.title())(required=True)