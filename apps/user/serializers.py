from rest_framework.serializers import ModelSerializer
from mighty.models.user import User

from mighty.apps.user.fields import serializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = serializer + ('detail_url',)
