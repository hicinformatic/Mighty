from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.module_loading import import_string

from mighty.views import ModelViewSet, ListView, DetailView
from mighty.models.grapher import Graph
from mighty.apps.grapher import filters, fields

@method_decorator(xframe_options_exempt, name='dispatch')
class GraphView(DetailView):
    no_permission = True
    fields = fields.graph
    template_name = 'mighty/graph.html'
    backend = None

    def get_header(self):
        return {'title': self.object.title, }

    def get_context_data(self, **kwargs):
        context = super(GraphView, self).get_context_data(**kwargs)
        backend = import_string(settings.GRAPHER_BACKEND)
        self.backend = backend(self.object)
        context.update({ 'templates': self.object.templates.all() })
        return context

class SvgView(GraphView):
    def get_context_data(self, **kwargs):
        context = super(SvgView, self).get_context_data(**kwargs)
        context.update({
            'css': self.backend.css['svg'],
            'html': self.backend.html['svg'],
            'directory': self.backend.directory['svg'],
            'js': self.backend.libraries('svg'),
        })
        return context

class CanvasView(GraphView):
    def get_context_data(self, **kwargs):
        context = super(CanvasView, self).get_context_data(**kwargs)
        context.update({
            'css': self.backend.css['canvas'],
            'html': self.backend.html['canvas'],
            'directory': self.backend.directory['canvas'],
            'js': self.backend.libraries('canvas'),
        })
        return context

class GraphViewSet(ModelViewSet):
    filter_model = filters.GraphFilter
    model = Graph
    list_display = ('__str__', 'image_html',)
    fields = fields.graph

    def __init__(self, model=None):
        super().__init__()
        self.addView('svg', SvgView, '%s/svg/')
        self.addView('canvas', CanvasView, '%s/canvas/')

if 'rest_framework' in settings.INSTALLED_APPS:
    from mighty.views.api import ApiModelViewSet
    from mighty.apps.grapher.serializers import GraphSerializer

    class GraphApiViewSet(ApiModelViewSet):
        filter_model = filters.GraphFilter
        model = Graph
        list_display = ('__str__', 'image_html',)
        fields = fields.graph
        queryset = Graph.objects.all()
        serializer_class = GraphSerializer

