from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()
class TwoFactorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return
        try:
            user = UserModel.objects.get(uid=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_code(password) and self.user_can_authenticate(user):
                if hasattr(request, 'META'):
                    user.get_client_ip(request)
                user.consume_code(password)
                return user

    def send_sms(self, user, backend_path):
        raise NotImplementedError('Method send_sms not implemented in %s' % type(self).__name__)

    def check_sms(self, email):
        raise NotImplementedError('Method check_sms not implemented in %s' % type(self).__name__)

    def send_email(self, user, backend_path):
        raise NotImplementedError('Method send_email not implemented in %s' % type(self).__name__)

    def check_email(self, user, backend_path):
        raise NotImplementedError('Method check_email not implemented in %s' % type(self).__name__)