from django.contrib import admin
from django.db import router, transaction
from django.contrib.admin.options import csrf_protect_m, IS_POPUP_VAR, TO_FIELD_VAR, get_content_type_for_model
from django.contrib.admin.utils import get_deleted_objects, unquote
from django.template.response import TemplateResponse
from django.contrib import messages
from django.urls import reverse, resolve
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import REDIRECT_FIELD_NAME, get_permission_codename
from django.contrib.auth.views import LoginView
from django.contrib.admin.forms import AdminAuthenticationForm
from django_json_widget.widgets import JSONEditorWidget

from functools import update_wrapper

from mighty.models import JSONField
from mighty.actions import enable_selected, disable_selected
from mighty import  _
from mighty import fields

fset_default = (_.f_default, {'fields': ('display', 'image')})
fset_infos = (_.f_infos, {'fields': (fields.readonly_fields)})

class InAlertListFilter(admin.SimpleListFilter):
    title = _.f_alerts
    parameter_name = 'inalert'

    def lookups(self, request, model_admin):
        return (('inalert', _.t_inalert),)

    def queryset(self, request, queryset):
        if self.value() == 'inerror': return queryset.filter(errors__isnull=False)

class InErrorListFilter(admin.SimpleListFilter):
    title = _.f_errors
    parameter_name = 'inerror'

    def lookups(self, request, model_admin):
        return (('inerror', _.t_inerror),)

    def queryset(self, request, queryset):
        if self.value() == 'inerror': return queryset.filter(errors__isnull=False)

class OverAdmin(admin.ModelAdmin):
    actions = [enable_selected, disable_selected]
    disable_selected_confirmation_template = None
    disable_confirmation_template = None
    enable_selected_confirmation_template = None
    enable_confirmation_template = None
    list_display = fields.list_display
    list_filter = (InErrorListFilter, InAlertListFilter) + fields.list_filter
    readonly_fields = fields.full
    search_fields = fields.search_fields
    save_on_top = True
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


    def has_enable_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('enable', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def has_disable_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('disable', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def save_model(self, request, obj, form, change):
        obj.update_by = request.user.username
        super(OverAdmin, self).save_model(request, obj, form, change)

    def disable_model(self, request, obj):
        """
        Given a model instance disable it from the database.
        """
        obj.disable()

    #@property
    #def view_on_site(self, obj):
    #    return obj.get_absolute_url if hasattr(obj, 'get_absolute_url') else False

    @transaction.atomic
    def disable_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        for o in queryset:
            o.disable()

    def log_enablion(self, request, object, object_repr):
        """
        Log that an object will be deleted. Note that this method must be
        called before the deletion.

        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, DELETION
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=object_repr,
            action_flag=DELETION,
        )

    def enable_model(self, request, obj):
        """
        Given a model instance enable it from the database.
        """
        obj.enable()

    @transaction.atomic
    def enable_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        for o in queryset:
            o.enable()

    def log_enablion(self, request, object, object_repr):
        """
        Log that an object will be deleted. Note that this method must be
        called before the deletion.

        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, DELETION
        return LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=object_repr,
            action_flag=DELETION,
        )

    def get_urls(self):
        from django.urls import path
        urls = super(OverAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        my_urls = [
            path('<path:object_id>/disable/', wrap(self.disable_view), name='%s_%s_disable' % info),
            path('<path:object_id>/enable/', wrap(self.enable_view), name='%s_%s_enable' % info),
        ]
        return my_urls + urls

    @csrf_protect_m
    def disable_view(self, request, object_id, extra_context=None):
        with transaction.atomic(using=router.db_for_write(self.model)):
            return self._disable_view(request, object_id, extra_context)

    def _disable_view(self, request, object_id, extra_context):
        "The 'disable' admin view for this model."
        opts = self.model._meta
        app_label = opts.app_label

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        obj = self.get_object(request, unquote(object_id), to_field)

        if not self.has_disable_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        # Populate disabled_objects, a data structure of all related objects that
        # will also be disabled.
        disabled_objects, model_count, perms_needed, protected = self.get_deleted_objects([obj], request)

        if request.POST and not protected:  # The user has confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = str(obj)
            attr = str(to_field) if to_field else opts.pk.attname
            obj_id = obj.serializable_value(attr)
            self.log_deletion(request, obj, obj_display)
            self.disable_model(request, obj)

            return self.response_disable(request, obj_display, obj_id)

        object_name = str(opts.verbose_name)

        if perms_needed or protected:
            title = _.cannotdisable % {"name": object_name}
        else:
            title = _.areyousure

        context = {
            **self.admin_site.each_context(request),
            'title': title,
            'object_name': object_name,
            'object': obj,
            'disabled_objects': disabled_objects,
            'model_count': dict(model_count).items(),
            'perms_lacking': perms_needed,
            'protected': protected,
            'opts': opts,
            'app_label': app_label,
            'preserved_filters': self.get_preserved_filters(request),
            'is_popup': IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET,
            'to_field': to_field,
            **(extra_context or {}),
        }
        return self.render_disable_form(request, context)

    def response_disable(self, request, obj_display, obj_id):
        """
        Determine the HttpResponse for the disable_view stage.
        """
        opts = self.model._meta

        if IS_POPUP_VAR in request.POST:
            popup_response_data = json.dumps({
                'action': 'disable',
                'value': str(obj_id),
            })
            return TemplateResponse(request, self.popup_response_template or [
                'admin/%s/%s/popup_response.html' % (opts.app_label, opts.model_name),
                'admin/%s/popup_response.html' % opts.app_label,
                'admin/popup_response.html',
            ], {
                'popup_response_data': popup_response_data,
            })

        self.message_user(
            request,
            _.disableok % {
                'name': opts.verbose_name,
                'obj': obj_display,
            },
            messages.SUCCESS,
        )

        if self.has_change_permission(request, None):
            post_url = reverse(
                'admin:%s_%s_changelist' % (opts.app_label, opts.model_name),
                current_app=self.admin_site.name,
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts}, post_url
            )
        else:
            post_url = reverse('admin:index', current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)

    def render_disable_form(self, request, context):
        opts = self.model._meta
        app_label = opts.app_label

        request.current_app = self.admin_site.name
        context.update(
            to_field_var=TO_FIELD_VAR,
            is_popup_var=IS_POPUP_VAR,
            media=self.media,
        )

        return TemplateResponse(
            request,
            self.disable_confirmation_template or [
                "admin/{}/{}/disable_confirmation.html".format(app_label, opts.model_name),
                "admin/{}/disable_confirmation.html".format(app_label),
                "admin/disable_confirmation.html",
            ],
            context,
        )

    @csrf_protect_m
    def enable_view(self, request, object_id, extra_context=None):
        with transaction.atomic(using=router.db_for_write(self.model)):
            return self._enable_view(request, object_id, extra_context)

    def _enable_view(self, request, object_id, extra_context):
        "The 'enable' admin view for this model."
        opts = self.model._meta
        app_label = opts.app_label

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        obj = self.get_object(request, unquote(object_id), to_field)

        if not self.has_enable_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        # Populate enabled_objects, a data structure of all related objects that
        # will also be enabled.
        enabled_objects, model_count, perms_needed, protected = self.get_deleted_objects([obj], request)

        if request.POST and not protected:  # The user has confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = str(obj)
            attr = str(to_field) if to_field else opts.pk.attname
            obj_id = obj.serializable_value(attr)
            self.log_deletion(request, obj, obj_display)
            self.enable_model(request, obj)

            return self.response_enable(request, obj_display, obj_id)

        object_name = str(opts.verbose_name)

        if perms_needed or protected:
            title = _.cannotenable % {"name": object_name}
        else:
            title = _.areyousure

        context = {
            **self.admin_site.each_context(request),
            'title': title,
            'object_name': object_name,
            'object': obj,
            'enabled_objects': enabled_objects,
            'model_count': dict(model_count).items(),
            'perms_lacking': perms_needed,
            'protected': protected,
            'opts': opts,
            'app_label': app_label,
            'preserved_filters': self.get_preserved_filters(request),
            'is_popup': IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET,
            'to_field': to_field,
            **(extra_context or {}),
        }
        return self.render_enable_form(request, context)

    def response_enable(self, request, obj_display, obj_id):
        """
        Determine the HttpResponse for the enable_view stage.
        """
        opts = self.model._meta

        if IS_POPUP_VAR in request.POST:
            popup_response_data = json.dumps({
                'action': 'enable',
                'value': str(obj_id),
            })
            return TemplateResponse(request, self.popup_response_template or [
                'admin/%s/%s/popup_response.html' % (opts.app_label, opts.model_name),
                'admin/%s/popup_response.html' % opts.app_label,
                'admin/popup_response.html',
            ], {
                'popup_response_data': popup_response_data,
            })

        self.message_user(
            request,
            _.enableok % {
                'name': opts.verbose_name,
                'obj': obj_display,
            },
            messages.SUCCESS,
        )

        if self.has_change_permission(request, None):
            post_url = reverse(
                'admin:%s_%s_changelist' % (opts.app_label, opts.model_name),
                current_app=self.admin_site.name,
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts}, post_url
            )
        else:
            post_url = reverse('admin:index', current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)

    def render_enable_form(self, request, context):
        opts = self.model._meta
        app_label = opts.app_label

        request.current_app = self.admin_site.name
        context.update(
            to_field_var=TO_FIELD_VAR,
            is_popup_var=IS_POPUP_VAR,
            media=self.media,
        )

        return TemplateResponse(
            request,
            self.enable_confirmation_template or [
                "admin/{}/{}/enable_confirmation.html".format(app_label, opts.model_name),
                "admin/{}/enable_confirmation.html".format(app_label),
                "admin/enable_confirmation.html",
            ],
            context,
        )

class AdminSite(admin.AdminSite):
    site_header = _.site_header
    index_title = _.index_title

    @never_cache
    def login(self, request, extra_context=None):
        current_url = resolve(request.path_info).url_name

        if request.method == 'GET' and self.has_permission(request):
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)

        context = dict(
            self.each_context(request),
            title=_.login,
            app_path=request.get_full_path(),
            username=request.user.get_username(),
            current_url=current_url,
            next_url=request.GET.get('next', '')
        )
        if (REDIRECT_FIELD_NAME not in request.GET and REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = reverse('admin:index', current_app=self.name)
        context.update(extra_context or {})

        defaults = {
            'extra_context': context,
            'authentication_form': AdminAuthenticationForm,
            'template_name': self.login_template or 'admin/login.html',
        }
        request.current_app = self.name
        return LoginView.as_view(**defaults)(request)

class FileInlineAdmin(admin.TabularInline):
    fields = ('the_file', 'mimetype')