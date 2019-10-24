from rest_framework.serializers import ModelSerializer
from mighty.models.user import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
