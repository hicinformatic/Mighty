from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.mixins import PermissionRequiredMixin


from mighty.functions import logger

guardian = True if 'guardian' in settings.INSTALLED_APPS else False
tpl = lambda a, n, t: ['%s/%s_%s.html' % (a, n, t), '%s/%s.html' % (a, t), '%s.html' % t, 'mighty/%s.html' % t]

class FormView(PermissionRequiredMixin, FormView):
    title = 'FormView'

    def get_template_names(self):
        app = str(self.model._meta.app_label).lower()
        name = str(self.model.__name__).lower()
        return self.template_name or tpl(app, name, 'form')

    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(FormView, self).get_context_data(**kwargs)
        context.update({'view': 'form', 'title': self.title})
        return context

class AddView(PermissionRequiredMixin, CreateView):
    title = 'AddView'

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm(self.model.perm(self.model, 'add')):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()

    def get_template_names(self):
        app = str(self.model._meta.app_label).lower()
        name = str(self.model.__name__).lower()
        return self.template_name or tpl(app, name, 'create')

    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(AddView, self).get_context_data(**kwargs)
        context.update({'opts': self.model._meta, 'view': 'create', 'title': self.title})
        return context

class ChangeView(PermissionRequiredMixin, UpdateView):
    slug_field = "uid"
    slug_url_kwarg = "uid"
    title = 'ChangeView'

    def get_template_names(self):
        app = str(self.model._meta.app_label).lower()
        name = str(self.model.__name__).lower()
        return self.template_name or tpl(app, name, 'change')

    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(ChangeView, self).get_context_data(**kwargs)
        context.update({'opts': self.model._meta, 'view': 'change', 'title': self.title})
        return context

    def get_success_url(self):
        return self.object.detail_url

class DeleteView(PermissionRequiredMixin, DeleteView):
    slug_field = "uid"
    slug_url_kwarg = "uid"
    title = 'DeleteView'

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm(self.model.perm(self.model, 'delete')):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()

    def get_template_names(self):
        app = str(self.model._meta.app_label).lower()
        name = str(self.model.__name__).lower()
        return self.template_name or tpl(app, name, 'delete')

    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(DeleteView, self).get_context_data(**kwargs)
        context.update({'opts': self.model._meta, 'view': 'delete', 'title': self.title})
        return context

    def get_success_url(self):
        return self.object.list_url

class EnableView(DeleteView):
    slug_field = "uid"
    slug_url_kwarg = "uid"
    title = 'EnableView'

    def get_template_names(self):
        app = str(self.model._meta.app_label).lower()
        name = str(self.model.__name__).lower()
        return self.template_name or tpl(app, name, 'enable')

    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(EnableView, self).get_context_data(**kwargs)
        context.update({'opts': self.model._meta, 'view': 'enable', 'title': self.title})
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.enable()
        return HttpResponseRedirect(success_url)

class DisableView(DeleteView):
    slug_field = "uid"
    slug_url_kwarg = "uid"
    title = 'DisableView'

    def get_template_names(self):
        app = str(self.model._meta.app_label).lower()
        name = str(self.model.__name__).lower()
        return self.template_name or tpl(app, name, 'disable')

    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(DisableView, self).get_context_data(**kwargs)
        context.update({'opts': self.model._meta, 'view': 'disable', 'title': self.title})
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.disable()
        return HttpResponseRedirect(success_url)

class ListView(PermissionRequiredMixin, ListView):
    template_name = None
    paginate_by = 100
    title = 'ListView'

    def get_template_names(self):
        app = str(self.model._meta.app_label).lower()
        name = str(self.model.__name__).lower()
        return self.template_name or tpl(app, name, 'list')

    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({'opts': self.model._meta, 'view': 'list', 'title': self.title, 'guardian': guardian, 'can_askfor': self.model.CAN_ASK_FOR_PERMISSIONS})
        return context

class DetailView(PermissionRequiredMixin, DetailView):
    slug_field = "uid"
    slug_url_kwarg = "uid"
    title = 'DetailView'

    def get_template_names(self):
        app = str(self.model._meta.app_label).lower()
        name = str(self.model.__name__).lower()
        return self.template_name or tpl(app, name, 'detail')

    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(DetailView, self).get_context_data(**kwargs)
        context.update({'opts': self.model._meta, 'view': 'detail', 'title': self.title, 'guardian': guardian, 'can_askfor': self.model.CAN_ASK_FOR_PERMISSIONS})
        return context

class TemplateView(PermissionRequiredMixin, TemplateView):
    title = 'TemplateView'

    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(TemplateView, self).get_context_data(**kwargs)
        context.update({'title': self.title, 'title': self.title, 'guardian': guardian})
        return context

class AdminView(object):
    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(AdminView, self).get_context_data(**kwargs)
        opts = self.model._meta
        context.update({
            'app_label': opts.app_label,
            'original': self.get_object(),
            'has_change_permission': self.request.user.has_perm(self.model.perm(self.model, 'change')),
            'guardian': guardian,
        })
        context.update(admin.site.each_context(self.request))
        return context

from copy import deepcopy
from django.urls import path, include
class ViewSet(object):
    views = {}
    excluded_views = ()

    def __init__(self):
        self.views = deepcopy(self.views)
        for k in self.excluded_views:
            del self.views[k]
  
    def view(self, view, *args, **kwargs):
        View = self.views[view]['view']
        class View(View):
            pass

        for k, v in kwargs.items():
            setattr(View, k, v)
        
        View.permission_required = (self.model().perm(view),)
        View.model = self.model
        View.fields = self.fields
        return View

    def name(self, view):
        return '%s-%s' % (str(self.model.__name__.lower()), view)

    def url(self, view, config):
        url = config['url']
        if view not in self.notuseid:
            url = url % self.slug
            if self.model.SHOW_DISPLAY_IN_URL:
                url = '%s%s/' % (url, '<str:display>')
        return url

    @property
    def urls(self):
        return [path(self.url(view, config), self.view(view).as_view(), name=self.name(view)) for view,config in self.views.items()]


class ModelViewSet(ViewSet):
    model = None
    fields = '__all__'
    notuseid = ['list', 'add']
    slug = '<uuid:uid>'
    views = {
        'list':    { 'view': ListView, 'url': '' },
        'add':     { 'view': AddView, 'url': 'add/' },
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