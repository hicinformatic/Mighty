from mighty.views import ViewSet
from mighty.models import User

class UserViewSet(ViewSet):
    model = User