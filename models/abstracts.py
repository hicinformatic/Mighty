from django.db import models

from mighty import fields, _
from mighty.models import JSONField
from mighty.functions import make_searchable, image_directory_path

from urllib.parse import quote_plus
from uuid import uuid4
from hashlib import sha256

PERM_ADD = 'add'
PERM_VIEW = 'view'
PERM_CHANGE = 'change'
PERM_DELETE = 'delete'
PERM_ENABLE = 'enable'
PERM_DISABLE = 'disable'
PERM_ADMINPERM = 'admin_perm'
PERM_ASKFORPERM = 'askfor_perm'

class ModelBase(models.Model):
    date_create = models.DateTimeField(_.f_date_create, auto_now_add=True, editable=False)
    date_update = models.DateTimeField(_.f_date_update, auto_now=True, editable=False)
    update_by = models.CharField(_.f_update_by, blank=True, editable=False, max_length=254, null=True)

    @property
    def app_label(self):
        return str(self._meta.app_label)

    @property
    def model_name(self):
        str(self.__class__.__name__)

    class Meta:
        abstract = True

class ModelUid(models.Model):
    uid = models.UUIDField(unique=True, default=uuid4, editable=False)

    class Meta:
        abstract = True

class ModelImage(models.Model):
    image = models.ImageField(upload_to=image_directory_path, default="none.jpg", blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def image_url(self):
        return self.image.url

class ModelDisplay(models.Model):
    display = models.CharField(_.f_display, blank=True, max_length=255, null=True)
    config_urldisplay = True

    class Meta:
        abstract = True

    def set_display(self):
        if self.display is None:
            self.display = str(self.__str__())

    def save(self, *args, **kwargs):
        self.set_display()
        super().save(*args, **kwargs)

class ModelToSearch(models.Model):
    to_search = models.TextField(_.f_to_search, db_index=True, blank=True, editable=False, null=True)

    class Meta:
        abstract = True

    def set_to_search(self):
        self.to_search = make_searchable(str(self.__str__()))

    def save(self, *args, **kwargs):
        self.set_to_search()
        super().save(*args, **kwargs)


class ModelSignHash(models.Model):
    signhash = models.CharField(_.f_signhash, db_index=True, blank=True, editable=False, max_length=254, null=True, unique=True)
    config_signhash = True

    class Meta:
        abstract = True

    def validate_unique(self, exclude=None):
        self.set_signhash()
        super().validate_unique(exclude)

    def fields(self):
        return self._meta.get_fields()

    def get_signhash(self, *args, **kwargs):
        if self.config_signhash:
            signhash = []
            for field in self.fields():
                if field in fields.notsignhash:
                    pass
                elif "notsignhash" in kwargs and field in kwargs["notsignhash"]:
                    pass
                elif field.__class__.__name__ == "ManyToManyField":
                    pass
                elif field.__class__.__name__ == "ManyToOneRel":
                    pass
                else:
                    signhash.append(getattr(self, field.name))
                if "fields" in kwargs:
                    for field in kwargs["fields"]: signash.append(field)
            return sha256(str(signhash).encode('utf-8')).hexdigest()
        else:
            return sha256(str(uuid4()).encode('utf-8')).hexdigest()

    def set_signhash(self, *args, **kwargs):
        signhash = self.get_signhash(*args, **kwargs)
        try:
            exist = self._meta.model.objects.get(signhash=signhash)
            if exist and exist.id != self.id:
                raise ValidationError(_.e_signhash)
        except self._meta.model.DoesNotExist:
            self.signhash = signhash

class ModelDisable(models.Model):
    is_disable = models.BooleanField(_.f_is_disable, default=False, editable=False)
    Qisdisable = models.Q(is_disable=False)
    Qisenable = models.Q(is_disable=True)

    class Meta:
        abstract = True

    @property
    def is_enable(self):
        return True if self.is_disable is False else False

    def disable(self, *args, **kwargs):
        self.is_disable = True
        self.save()

    def enable(self, *args, **kwargs):
        self.is_disable = False
        self.save()

class ModelAlert(models.Model):
    alerts = JSONField(_.f_alerts, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def is_in_alert(self):
        return True if alert is not None else False

class ModelError(models.Model):
    errors = JSONField(_.f_errors, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def is_in_error(self):
        return True if error is not None else False

class ModelPermissions(models.Model):
    config_askfor = True

    def perm(self, perm):
        return '%s.%s_%s' % (str(self.app_label).lower(), perm, str(self.model_name).lower())

    class Meta:
        abstract = True
        default_permissions = (
            PERM_ADD,
            PERM_VIEW,
            PERM_CHANGE,
            PERM_DELETE,
            PERM_ENABLE,
            PERM_DISABLE,
            PERM_ADMINPERM,
            PERM_ASKFORPERM,
        )
    
class ModelFull(ModelUid, ModelBase, ModelDisable, ModelError, ModelAlert, ModelToSearch, ModelSignHash, ModelImage, ModelDisplay, ModelPermissions):
    class Meta(ModelPermissions.Meta):
        abstract = True
