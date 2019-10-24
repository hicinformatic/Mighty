from rest_framework.serializers import ModelSerializer
from mighty.models.grapher import Graph

class GraphSerializer(ModelSerializer):
    class Meta:
        model = Graph
        fields = ('__all__')
