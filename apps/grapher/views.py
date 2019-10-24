from django.conf import settings
from mighty.views import ModelViewSet, ListView, DetailView
from mighty.models.grapher import Graph
from mighty.apps.grapher import filters

fields = (
        "title",
        "Bar",
        "Bipolar",
        "Funnel",
        "Gauge",
        "HorizontalBar",
        "HorizontalProgressbars",
        "Line",
        "Pie",
        "Radar",
        "Rose",
        "Scatter",
        "SemicircularProgressbars",
        "VerticalProgressbars",
        "Waterfall",
        "Donut",
        "Fuel",
        "Gantt",
        "Meter",
        "Odometer",
        "Radialscatter",
        "Thermometer",
    )

class SVGGraph(DetailView):
    fields = fields

    def get_header(self):
        return {'title': self.object.title, }

class GraphViewSet(ModelViewSet):
    filter_model = filters.GraphFilter
    model = Graph
    list_display = ('__str__', 'image_html',)
    fields = fields

    def __init__(self, model=None):
        super().__init__()
        self.addView('svg', SVGGraph, '%s/svg/')

if 'rest_framework' in settings.INSTALLED_APPS:
    from mighty.views.api import ApiModelViewSet
    from mighty.apps.grapher.serializers import GraphSerializer

    class GraphApiViewSet(ApiModelViewSet):
        filter_model = filters.GraphFilter
        model = Graph
        list_display = ('__str__', 'image_html',)
        fields = fields
        queryset = Graph.objects.all()
        serializer_class = GraphSerializer

