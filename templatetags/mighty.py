from django import template
from django.conf import settings

guardian = False
if 'guardian' in settings.INSTALLED_APPS:
    from guardian.core import ObjectPermissionChecker
    guardian = True
 
register = template.Library()

@register.simple_tag
def has_perm(obj, user, perm):
    return ObjectPermissionChecker(user).has_perm(perm, obj) if guardian else user.has_perm(obj.perm(perm))