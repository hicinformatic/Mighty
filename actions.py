from django.utils.translation import gettext_lazy as _
from django.contrib.admin.utils import model_ngettext
from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from django.contrib import messages

def disable_selected(modeladmin, request, queryset):
    """
    Default action which disables the selected objects.

    This action first displays a confirmation page which shows all the
    disableable objects, or, if the user has no permission one of the related
    childs (foreignkeys), a "permission denied" message.

    Next, it disables all selected objects and redirects back to the change list.
    """
    opts = modeladmin.model._meta
    app_label = opts.app_label

    # Populate disableable_objects, a data structure of all related objects that
    # will also be disabled.
    disableable_objects, model_count, perms_needed, protected = modeladmin.get_deleted_objects(queryset, request)

    # The user has already confirmed the enablion.
    # Do the enablion and return None to display the change list view again.
    if request.POST.get('post') and not protected:
        if perms_needed:
            raise PermissionDenied
        n = queryset.count()
        if n:
            for obj in queryset:
                obj_display = str(obj)
                modeladmin.log_enablion(request, obj, obj_display)
            modeladmin.disable_queryset(request, queryset)
            modeladmin.message_user(request, _("Successfully disabled %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(modeladmin.opts, n)
            }, messages.SUCCESS)
        # Return None to display the change list page again.
        return None

    objects_name = model_ngettext(queryset)

    if perms_needed or protected:
        title = _("Cannot disable %(name)s") % {"name": objects_name}
    else:
        title = _("Are you sure?")

    context = {
        **modeladmin.admin_site.each_context(request),
        'title': title,
        'objects_name': str(objects_name),
        'disableable_objects': [disableable_objects],
        'model_count': dict(model_count).items(),
        'queryset': queryset,
        'perms_lacking': perms_needed,
        'protected': protected,
        'opts': opts,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'media': modeladmin.media,
    }

    request.current_app = modeladmin.admin_site.name

    # Display the confirmation page
    return TemplateResponse(request, modeladmin.disable_selected_confirmation_template or [
        "admin/mighty/disable_selected_confirmation.html"
    ], context)
disable_selected.allowed_permissions = ('change',)
disable_selected.short_description = _("Disable selected %(verbose_name_plural)s")

def enable_selected(modeladmin, request, queryset):
    """
    Default action which enables the selected objects.

    This action first displays a confirmation page which shows all the
    enableable objects, or, if the user has no permission one of the related
    childs (foreignkeys), a "permission denied" message.

    Next, it enables all selected objects and redirects back to the change list.
    """
    opts = modeladmin.model._meta
    app_label = opts.app_label

    # Populate enableable_objects, a data structure of all related objects that
    # will also be enabled.
    enableable_objects, model_count, perms_needed, protected = modeladmin.get_deleted_objects(queryset, request)

    # The user has already confirmed the enablion.
    # Do the enablion and return None to display the change list view again.
    if request.POST.get('post') and not protected:
        if perms_needed:
            raise PermissionDenied
        n = queryset.count()
        if n:
            for obj in queryset:
                obj_display = str(obj)
                modeladmin.log_enablion(request, obj, obj_display)
            modeladmin.enable_queryset(request, queryset)
            modeladmin.message_user(request, _("Successfully enabled %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(modeladmin.opts, n)
            }, messages.SUCCESS)
        # Return None to display the change list page again.
        return None

    objects_name = model_ngettext(queryset)

    if perms_needed or protected:
        title = _("Cannot enable %(name)s") % {"name": objects_name}
    else:
        title = _("Are you sure?")

    context = {
        **modeladmin.admin_site.each_context(request),
        'title': title,
        'objects_name': str(objects_name),
        'enableable_objects': [enableable_objects],
        'model_count': dict(model_count).items(),
        'queryset': queryset,
        'perms_lacking': perms_needed,
        'protected': protected,
        'opts': opts,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'media': modeladmin.media,
    }

    request.current_app = modeladmin.admin_site.name

    # Display the confirmation page
    return TemplateResponse(request, modeladmin.enable_selected_confirmation_template or [
        "admin/%s/%s/enable_selected_confirmation.html" % (app_label, opts.model_name),
        "admin/%s/enable_selected_confirmation.html" % app_label,
        "admin/enable_selected_confirmation.html"
    ], context)
enable_selected.allowed_permissions = ('change',)
enable_selected.short_description = _("Enable selected %(verbose_name_plural)s")