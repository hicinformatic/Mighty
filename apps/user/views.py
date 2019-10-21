from mighty.views import ModelViewSet, DetailView
from mighty.models.user import User
from mighty.apps.user import filters

class UserMe(DetailView):
    fields = ('last_name', 'first_name', 'email', 'phone', 'gender',)

    def get_header(self):
        return {
            'title': 'me',
        }

    def get_object(self, queryset=None):
        return User.objects.all().first()

class UserViewSet(ModelViewSet):
    model = User
    filter_model = filters.UserFilter
    fields = ('last_name', 'first_name', 'email', 'phone', 'gender',)
    add_fields = ('username', 'last_name', 'first_name', 'email', 'phone', 'gender',)

    def __init__(self, model=None):
        super().__init__()
        self.addNotuseid('me')
        self.addView('me', UserMe, 'me/')