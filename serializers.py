from django.conf import settings
from rest_framework.serializers import ModelSerializer
from mighty.fields import file_fields

class FileSerializer(ModelSerializer):
    class Meta:
        fields = file_fields