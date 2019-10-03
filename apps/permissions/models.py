from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from mighty.apps.permissions import _
from mighty.apps.user import _ as _u


UserModel = get_user_model()
WAITING = 'waiting'
VALIDATE = 'validate'
INVALIDATE = 'invalidate'
choices_permission_status = ((WAITING, _.c_waiting), (VALIDATE, _.c_validate), (INVALIDATE, _.c_invalidate))
class PermissionAsk(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_permissionask')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='permission_permissionask')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='content_type_permissionask')
    cid = models.BigIntegerField(db_index=True, blank=True, null=True)
    cuid = models.UUIDField(db_index=True, blank=True, null=True)
    status = models.CharField(_.f_status, choices=choices_permission_status, max_length=20, default=WAITING)
    ipv4 = models.GenericIPAddressField(_u.f_ipv4, blank=True, null=True, editable=False)
    ipv6 = models.GenericIPAddressField(_u.f_ipv6, blank=True, null=True, editable=False)

    class Meta:
        abstract = True
        verbose_name = _.v_permissionask
        verbose_name_plural = _.vp_permissionask
        unique_together = ('user', 'permission', 'content_type')

    def __str__(self):
        return '%s(%s) | %s' % (self.content_type, self.user, self.permission)