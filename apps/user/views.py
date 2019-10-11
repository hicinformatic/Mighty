from mighty.views import ModelViewSet
from mighty.models.user import Nationality, User

class NationalityViewSet(ModelViewSet):
    model = Nationality

class UserViewSet(ModelViewSet):
    model = User
    fields = ('email', 'phone', 'gender',)