from django import template
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
register = template.Library()

guardian = False
if 'guardian' in settings.INSTALLED_APPS:
    from guardian.core import ObjectPermissionChecker
    guardian = True

@register.simple_tag(name='has_perm')
def has_perm(obj, user, perm):
    if hasattr(obj, 'perm'):
        return ObjectPermissionChecker(user).has_perm(perm, obj) if guardian else user.has_perm(obj.perm(perm))
    else:
        return False

@register.simple_tag(name='field_name')
def field_name(obj, field):
    if field == '__str__':
        return obj._meta.verbose_name
    else:
        try:
            return obj._meta.get_field(field).verbose_name
        except FieldDoesNotExist:
            try:
                return getattr(obj, field).short_description
            except Exception:
                pass
    return ""

@register.simple_tag(name='field_value')
def field_value(obj, field):
    if field == '__str__':
        return str(obj)
    else:
        attr = getattr(obj, field)
    attr = attr() if callable(attr) else attr
    return "" if attr is None else attr

@register.filter(name='add_attr')
def add_attr(field, css):
    attrs = {}
    definition = css.split(',')
    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, val = d.split(':')
            attrs[key] = val
    return field.as_widget(attrs=attrs)

@register.simple_tag(name='number_hread')
def number_hread(number, separator=None):
    return '{:,}'.format(number).replace(",", separator) if separator else '{:,}'.format(number)
