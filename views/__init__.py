from django.conf import settings
from django.contrib import admin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, StreamingHttpResponse

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.exceptions import PermissionDenied
from django.urls import path, include

from copy import deepcopy
from mighty.functions import logger
from mighty import _

import csv

guardian = True if 'guardian' in settings.INSTALLED_APPS else False
tpl = lambda a, n, t: [
    '%s/%s_%s.html' % (a, n, t), '%s/%s/%s.html' % (a, n, t),
    '%s_%s.html' % (a, t), '%s/%s.html' % (a, t), '%s/actions/%s.html' % (a, t),
    '%s_%s.html' % (n, t), '%s/%s.html' % (n, t), '%s/actions/%s.html' % (n, t),
    '%s.html' % t,
]

generator = [
    'add',
    'list',
    'admin_add',
    'admin_list',
    'admin_change',
    'detail',
    'change',
    'delete',
    'enable',
    'disable',
    'export',
    'import',
    "logout",
    "login",
    "admin",
    "admin_view",
    "clear",
    "home",
]

class BaseView(PermissionRequiredMixin):
    filter_model = None
    slug_field = "uid"
    slug_url_kwarg = "uid"
    fields = ()
    paginate_by = 100
    template_name = None
    permission_required = ()
    no_permission = False
    app_label = None
    model_name = None
    add_to_context = {}

    def has_object(self):
        return True if hasattr(self, 'object') and self.object is not None else False

    def has_model(self):
        return True if hasattr(self, 'model') and self.model is not None else False

    def get_template_names(self):
        app_label = model_name = None
        if self.has_model():
            app_label = self.app_label or str(self.model._meta.app_label).lower()
            model_name = self.model_name or str(self.model.__name__).lower()
        if self.app_label: app_label = self.app_label
        if self.model_name: model_name = self.model_name
        self.template_name = self.template_name or tpl(app_label, model_name, str(self.__class__.__name__).lower())
        logger("mighty", "info", "template: %s" % self.template_name)
        return self.template_name

    def get_meta(self, translate, view):
        meta = {}
        if view in translate and self.has_model(): meta.update({ 'title': '%s | %s' % (self.model._meta.verbose_name, translate[view])})
        elif view in translate: meta.update({'title': translate[view]} )
        return meta

    def get_urls(self):
        if self.has_model():
            model = self.object if self.has_object() else self.model()
            return {url: getattr(model, '%s_url' % url) for url in generator if hasattr(model, '%s_url' % url)}
        return {}

    def get_permissions(self):
        if self.has_model():
            model = self.object if self.has_object() else self.model()
            return {'has_%s_permission' % perm: self.request.user.has_perm(model.perm(perm)) for perm in model.title}
        return {}

    def get_translate(self):
        return {
            "titles": {url: getattr(_, 't_%s' % url) for url in generator if hasattr(_, 't_%s' % url)},
            "templates": {url: getattr(_, 'tpl_%s' % url) for url in generator if hasattr(_, 'tpl_%s' % url)},
        }

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context.update({
            'options': { 'guardian': guardian, 'debug': settings.DEBUG, },
            'has_object': self.has_object(),
            'translate': self.get_translate(),
            'links': self.get_urls(),
            'view': self.__class__.__name__,
            'fields': self.fields,
        })
        context.update(self.get_permissions())
        context.update(self.add_to_context)
        context.update({ 'meta': self.get_meta(context['translate']['titles'], context['view']),})
        if self.has_model(): context.update({'opts': self.model._meta})
        return context

class FormView(BaseView, FormView):
    pass

class AddView(BaseView, CreateView):
    pass

class DetailView(BaseView, DetailView):
    pass

class TemplateView(BaseView, TemplateView):
    pass    

class ListView(BaseView, ListView):
    def get_queryset(self):
        if self.is_ajax: return self.model.objects.none()
        if self.filter_model is None: return super().get_queryset()
        else: queryset, q = self.filter_model(self.request)
        return queryset.filter(q)

class ChangeView(BaseView, UpdateView):
    def get_success_url(self):
        return self.object.detail_url

class DeleteView(BaseView, DeleteView):
    def get_success_url(self):
        return self.object.list_url

class EnableView(DeleteView):
    def get_success_url(self):
        return self.object.detail_url

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.enable()
        return HttpResponseRedirect(success_url)

class DisableView(EnableView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.disable()
        return HttpResponseRedirect(success_url)

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

class ExportView(ListView):
    def iter_items(self, items, pseudo_buffer):
        writer = csv.writer(pseudo_buffer)
        yield writer.writerow(self.fields)
        for item in items:
            yield writer.writerow(item)

    def render_to_response(self, context, **response_kwargs):
        frmat = self.request.GET.get('format', '')
        response = StreamingHttpResponse(
            streaming_content=(self.iter_items(self.model.objects.all().values_list(*self.fields), Echo())),
            content_type='text/csv',
        )
        response['Content-Disposition'] = 'attachment;filename=items.csv'
        return response

class AdminView(object):
    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(AdminView, self).get_context_data(**kwargs)
        opts = self.model._meta
        context.update({
            'opts': opts,
            'app_label': opts.app_label,
            'original': self.get_object(),
            'has_change_permission': self.request.user.has_perm(self.model.perm(self.model, 'change')),
            'guardian': guardian,
        })
        context.update(admin.site.each_context(self.request))
        return context

class ViewSet(object):
    views = {}
    fields = ()
    excluded_views = ()
    notuseid = []
    filter_model = None
    add_to_context = {}
    is_ajax = False

    def __init__(self):
        self.views = deepcopy(self.views)
        for k in self.excluded_views:
            del self.views[k]
  
    def view(self, view, *args, **kwargs):
        View = type(view, (self.views[view]['view'],), {})
        View.model = self.model
        View.fields = self.fields
        View.add_to_context = getattr(self, '%s_add_to_context' % view) if hasattr(self, '%s_add_to_context' % view) else self.add_to_context
        View.is_ajax = getattr(self, '%s_is_ajax' % view) if hasattr(self, '%s_is_ajax' % view) else self.is_ajax
        View.fields = getattr(self, '%s_fields' % view) if hasattr(self, '%s_fields' % view) else self.fields
        View.no_permission = getattr(self, '%s_no_permission' % view) if hasattr(self, '%s_no_permission' % view) else False
        if not View.no_permission: View.permission_required = (self.model().perm(view),)
        for k, v in kwargs.items(): setattr(View, k, v)
        if view == 'list':
            if self.filter_model is not None:
                View.filter_model = self.filter_model
        return View

    def name(self, view):
        return '%s-%s' % (str(self.model.__name__.lower()), view)

    def url(self, view, config):
        if view not in self.notuseid:
            return '%s%s/' % (config['url'] % self.slug, '<str:display>') if self.model.SHOW_DISPLAY_IN_URL else config['url'] % self.slug
        return config['url']

    def addView(self, name, view, url):
        self.views[name] = { 'view': view, 'url': url }

    def addNotuseid(self, view):
        self.notuseid.append(view)

    @property
    def urls(self):
        return [path(self.url(view, config), self.view(view).as_view(), name=self.name(view)) for view,config in self.views.items()]


class ModelViewSet(ViewSet):
    model = None

    fields = '__all__'
    notuseid = ['list', 'add', 'export', 'import']
    slug = '<uuid:uid>'
    views = {
        'list':    { 'view': ListView, 'url': '' },
        'add':     { 'view': AddView, 'url': 'add/' },
        'export': { 'view': ExportView, 'url': 'export/' },
        #'import': { 'view': ImportView, 'url': 'import/<str:format>/' },
        'detail':  { 'view': DetailView, 'url': '%s/detail/' },
        'change':  { 'view': ChangeView, 'url': '%s/change/' },
        'delete':  { 'view': DeleteView, 'url': '%s/delete/' },
        'enable':  { 'view': EnableView, 'url': '%s/enable/' },
        'disable': { 'view': DisableView, 'url': '%s/disable/' },
    }

    def __init__(self, model=None):
        super().__init__()
        if model is not None:
            self.model = model