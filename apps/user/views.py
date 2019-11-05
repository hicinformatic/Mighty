from django.conf import settings
from mighty.views import ModelViewSet, DetailView
from mighty.models.user import User
from mighty.apps.user import filters

class UserMe(DetailView):
    fields = ('last_name', 'first_name', 'email', 'phone', 'gender',)

    def get_header(self):
        return {'title': 'me',}

    def get_object(self, queryset=None):
        return self.request.user

class UserViewSet(ModelViewSet):
    model = User
    filter_model = filters.UserFilter
    fields = ('last_name', 'first_name', 'email', 'phone', 'gender',)
    add_fields = ('username', 'last_name', 'first_name', 'email', 'phone', 'gender',)

    def __init__(self, model=None):
        super().__init__()
        self.addNotuseid('me')
        self.addView('me', UserMe, 'me/')

if 'rest_framework' in settings.INSTALLED_APPS:
    from mighty.views.api import ApiModelViewSet
    from mighty.apps.user.serializers import UserSerializer

    class UserApiViewSet(ApiModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        filter_model = filters.UserFilter
        model = User
        serializer_class = UserSerializer
