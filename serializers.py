from django.conf import settings
from rest_framework.serializers import ModelSerializer
from mighty.fields import files

class FileSerializer(ModelSerializer):
    class Meta:
        fields = files