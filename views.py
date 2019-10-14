from django.conf import settings
from django.contrib import admin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.exceptions import PermissionDenied
from django.urls import path, include

from copy import deepcopy


from mighty.functions import logger
from mighty import _

guardian = True if 'guardian' in settings.INSTALLED_APPS else False
tpl = lambda a, n, t: ['%s/%s_%s.html' % (a, n, t), '%s/%s.html' % (a, t), '%s.html' % t, 'mighty/%s.html' % t, 'mighty/actions/%s.html' % t]

class BaseView(PermissionRequiredMixin):
    template_name = None
    slug_field = "uid"
    slug_url_kwarg = "uid"
    paginate_by = 100
    permission_required = ()

    def has_object(self):
        return True if hasattr(self, 'object') and self.object is not None else False

    def get_options(self):
        return {
            'guardian': guardian,
        }

    def get_header(self):
        return {
            'title': '%s | %s' % (self.model._meta.verbose_name, self.get_titles()[self.__class__.__name__])
        }

    def get_titles(self):
        return {
            'add': _.t_add,
            'detail': _.t_detail,
            'list': _.t_list,
            'change': _.t_change,
            'delete': _.t_delete,
            'enable': _.t_enable,
            'disable': _.t_disable,
        }

    def get_urls(self):
        hasobject = self.has_object()
        model = self.object if hasobject else self.model()
        urls = {
            'add': model.add_url,
            'list': model.list_url,
            'admin': {
                'add': model.admin_add_url,
                'list': model.admin_list_url,
                'change': model.admin_change_url,
            }
        }
        if hasobject:
            urls.update({
                'detail': model.detail_url,
                'change': model.change_url,
                'delete': model.delete_url,
                'enable': model.enable_url,
                'disable': model.disable_url,
            })
        return urls

    def get_permissions(self):
        model = self.object if self.has_object() else self.model()
        return {
            'has_add_permission': self.request.user.has_perm(model.perm('add')),
            'has_list_permission': self.request.user.has_perm(model.perm('list')),
            'has_detail_permission': self.request.user.has_perm(model.perm('detail')),
            'has_change_permission': self.request.user.has_perm(model.perm('change')),
            'has_delete_permission': self.request.user.has_perm(model.perm('delete')),
            'has_enable_permission': self.request.user.has_perm(model.perm('enable')),
            'has_disable_permission': self.request.user.has_perm(model.perm('disable')),
        }

    def get_template_names(self):
        app = str(self.model._meta.app_label).lower()
        name = str(self.model.__name__).lower()
        return self.template_name or tpl(app, name, self.__class__.__name__)

    def get_questions(self):
        return {
            "disable": _.tpl_disable,
            "enable": _.tpl_enable,
            "delete": _.tpl_delete,
            'admin_view':  _.tpl_admin_view,
        }

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context.update({
            'header': self.get_header(),
            'titles': self.get_titles(),
            'options': self.get_options(),
            'links': self.get_urls(),
            'has_object': self.has_object(),
            'questions': self.get_questions(),
            'view': self.__class__.__name__,
        })
        context.update(self.get_permissions())
        if hasattr(self, "model"):
            context.update({'meta': self.model._meta})
        if hasattr(self, 'list_display'):
            context.update({'list_display': self.list_display})
        if hasattr(self, 'fields'):
            context.update({'fields': self.fields})
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
    filter_model = None

    def get_queryset(self):
        if self.filter_model is None:
            return super().get_queryset()
        else:
            queryset, q = self.filter_model(self.request)
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

class ViewSet(object):
    views = {}
    excluded_views = ()
    notuseid = []
    filter_model = None
    fields = ()
    list_display = ('__str__',)
    add_fields = None
    change_fields = None
    detail_fields = None
    form_fields = None

    def __init__(self):
        self.views = deepcopy(self.views)
        for k in self.excluded_views:
            del self.views[k]
  
    def view(self, view, *args, **kwargs):
        View = type(view, (self.views[view]['view'],), {})

        for k, v in kwargs.items():
            setattr(View, k, v)
        
        View.permission_required = (self.model().perm(view),)
        View.model = self.model
        View.fields = self.fields
        if view == 'list':
            View.list_display = self.list_display
            if self.filter_model is not None:
                View.filter_model = self.filter_model
        if view == 'add':
            View.fields = self.fields if self.add_fields is None else self.add_fields
        if view == 'change':
            View.fields = self.fields if self.change_fields is None else self.change_fields
        if view == 'detail':
            View.fields = self.fields if self.detail_fields is None else self.detail_fields

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