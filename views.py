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

class CreateView(PermissionRequiredMixin, CreateView):
    title = 'CreateView'

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
        context = super(CreateView, self).get_context_data(**kwargs)
        context.update({'opts': self.model._meta, 'view': 'create', 'title': self.title})
        return context

class UpdateView(PermissionRequiredMixin, UpdateView):
    slug_field = "uid"
    slug_url_kwarg = "uid"
    title = 'UpdateView'

    def get_template_names(self):
        app = str(self.model._meta.app_label).lower()
        name = str(self.model.__name__).lower()
        return self.template_name or tpl(app, name, 'update')

    def get_context_data(self, **kwargs):
        logger("mighty", "info", "view: %s" % self.__class__.__name__, self.request.user)
        context = super(UpdateView, self).get_context_data(**kwargs)
        context.update({'opts': self.model._meta, 'view': 'update', 'title': self.title})
        return context

    def get_success_url(self):
        return self.object.get_absolute_url

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
        return self.object.get_list_url

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
        context.update({'opts': self.model._meta, 'view': 'list', 'title': self.title, 'guardian': guardian, 'can_askfor': self.model.config_askfor})
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
        context.update({'opts': self.model._meta, 'view': 'detail', 'title': self.title, 'guardian': guardian, 'can_askfor': self.model.config_askfor})
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

class ViewSet:
    model = None
    fields = '__all__'

    @classmethod
    def CreateView(self, *args, **kwargs):
        view = CreateView
        view.fields = self.fields
        view.model = self.model
        view.permission_required = (self.model().perm('add'),)
        return view.as_view()

    @classmethod
    def UpdateView(self, *args, **kwargs):
        view = UpdateView
        view.fields = self.fields
        view.model = self.model
        view.permission_required = (self.model().perm('change'),)
        return view.as_view()

    @classmethod
    def DeleteView(self, *args, **kwargs):
        view = DeleteView
        view.model = self.model
        view.permission_required = (self.model().perm('delete'),)
        return view.as_view()

    @classmethod
    def EnableView(self, *args, **kwargs):
        view = EnableView
        view.model = self.model
        view.permission_required = (self.model().perm('enable'),)
        return view.as_view()

    @classmethod
    def DisableView(self, *args, **kwargs):
        view = DisableView
        view.model = self.model
        view.permission_required = (self.model().perm('disable'),)
        return view.as_view()

    @classmethod
    def ListView(self, *args, **kwargs):
        view = ListView
        view.model = self.model
        view.permission_required = (self.model().perm('list'),)
        return view.as_view()

    @classmethod
    def DetailView(self, *args, **kwargs):
        view = DetailView
        view.model = self.model
        view.permission_required = (self.model().perm('view'),)
        return view.as_view()