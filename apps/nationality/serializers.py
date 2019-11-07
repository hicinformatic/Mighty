from rest_framework.serializers import ModelSerializer
from mighty.models.nationality import Nationality

class NationalitySerializer(ModelSerializer):
    class Meta:
        model = Nationality
        fields = ('country', 'alpha2', 'alpha3', 'numeric', 'image_url',)