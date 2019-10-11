from mighty.views import ModelViewSet, ListView
from mighty.models.user import User
from mighty.apps.user import filters

class UserViewSet(ModelViewSet):
    model = User
    filter_model = filters.UserFilter
    fields = ('last_name', 'first_name', 'email', 'phone', 'gender',)
    add_fields = ('username', 'last_name', 'first_name', 'email', 'phone', 'gender',)