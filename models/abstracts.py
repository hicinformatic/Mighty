from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html
from django.utils.text import get_valid_filename

from mighty import fields, _
from mighty.models import JSONField
from mighty.functions import make_searchable, image_directory_path, file_directory_path, test

from urllib.parse import quote_plus
from uuid import uuid4
from hashlib import sha256
import os

PERM_ADD = 'add'
PERM_DETAIL = 'detail'
PERM_LIST = 'list'
PERM_CHANGE = 'change'
PERM_DELETE = 'delete'
PERM_ENABLE = 'enable'
PERM_DISABLE = 'disable'
PERM_EXPORT = 'export'
PERM_IMPORT = 'import'
PERM_ALERT = 'alert'
PERM_ERROR = 'error'
PERM_ADMINPERM = 'admin_perm'
PERM_ASKFORPERM = 'askfor_perm'

class ModelBase(models.Model):
    date_create = models.DateTimeField(_.f_date_create, auto_now_add=True, editable=False)
    date_update = models.DateTimeField(_.f_date_update, auto_now=True, editable=False)
    update_by = models.CharField(_.f_update_by, blank=True, editable=False, max_length=254, null=True)
    title = {
        PERM_ADD: _.t_add,
        PERM_LIST: _.t_list,
        PERM_DETAIL: _.t_detail,
        PERM_CHANGE: _.t_change,
        PERM_DELETE: _.t_delete,
        PERM_ENABLE: _.t_enable,
        PERM_DISABLE: _.t_disable, 
        PERM_EXPORT: _.t_export,
        PERM_IMPORT: _.t_import,
        PERM_ALERT: _.t_alert,
        PERM_ERROR: _.t_error,
        PERM_ADMINPERM: _.t_admin_perm,
        PERM_ASKFORPERM: _.t_askfor_perm,
    }

    SHOW_DISPLAY_IN_URL = False
    GENERATE_SIGNHASH = False
    CAN_ASK_FOR_PERMISSIONS = False

    class Meta:
        abstract = True
        default_permissions = (
            PERM_ADD,
            PERM_DETAIL,
            PERM_LIST,
            PERM_CHANGE,
            PERM_DELETE,
            PERM_ENABLE,
            PERM_DISABLE, 
            PERM_EXPORT,
            PERM_IMPORT,
            PERM_ALERT,
            PERM_ERROR,
            PERM_ADMINPERM,
            PERM_ASKFORPERM,
        )

    def fields(self, excludes=[]):
        return [field for field in self._meta.get_fields() if field.__class__.__name__ not in excludes]

    @property
    def app_label(self):
        return str(self._meta.app_label)

    @property
    def model_name(self):
        return str(self.__class__.__name__)

    def get_url(self, action, kwargs={}):
        try:
            return reverse('%s:%s-%s' % (self.app_label.lower(), self.model_name.lower(), action), kwargs=kwargs)
        except NoReverseMatch:
            return '#'

    def get_admin_url(self, action, args=()):
        try:
            return reverse('admin:%s_%s_%s' % (self.app_label.lower(), self.model_name.lower(), action), args=args)
        except NoReverseMatch:
            return '#'

    @property
    def admin_list_url(self):
        return self.get_admin_url('changelist')

    @property
    def admin_add_url(self):
        return self.get_admin_url('add')

    @property
    def admin_change_url(self):
        return self.get_admin_url('change', args=(self.id,))

    @property
    def add_url(self):
        return self.get_url('add')

    @property
    def list_url(self):
        return self.get_url('list')

    @property
    def detail_url(self):
        kwargs = {'uid': str(self.uid)} if hasattr(self, 'uid') else {'pk': str(self.pk)}
        if self.SHOW_DISPLAY_IN_URL: kwargs['display'] = quote_plus(self.display)
        return self.get_url('detail', kwargs=kwargs)

    @property
    def change_url(self):
        kwargs = {'uid': str(self.uid)} if hasattr(self, 'uid') else {'pk': str(self.pk)}
        if self.SHOW_DISPLAY_IN_URL: kwargs['display'] = quote_plus(self.display)
        return self.get_url('change', kwargs=kwargs)

    @property
    def delete_url(self):
        kwargs = {'uid': str(self.uid)} if hasattr(self, 'uid') else {'pk': str(self.pk)}
        if self.SHOW_DISPLAY_IN_URL: kwargs['display'] = quote_plus(self.display)
        return self.get_url('delete', kwargs=kwargs)

    def get_url_html(self, action, title=None):
        return format_html('<a href="%s">%s</a>' % (getattr(self, '%s_url' % action), self.__str__() if title is None else title))

    @property
    def add_url_html(self):
        return self.get_url_html('add', self.title['add'])

    @property
    def list_url_html(self):
        return self.get_url_html('list', self.title['list'])

    @property
    def detail_url_html(self):
        return self.get_url_html('detail')

    @property
    def change_url_html(self):
        return self.get_url_html('change', self.title['change'])

    @property
    def delete_url_html(self):
        return self.get_url_html('delete', self.title['delete'])

class ModelUid(models.Model):
    uid = models.UUIDField(unique=True, default=uuid4, editable=False)

    class Meta:
        abstract = True

IMAGE_DEFAULT = "none.jpg"
class ModelImage(models.Model):
    image = models.ImageField(upload_to=image_directory_path, default=IMAGE_DEFAULT, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def image_html(self):
        return format_html('<img src="%s" title="%s">' % (self.image.url, str(self)))

    @property
    def image_url(self):
        return self.image.url

    @property
    def imagename(self):
        return os.path.basename(self.image.name)

    @property
    def valid_imagename(self):
        return get_valid_filename(self.imagename)

    @property
    def image_extension(self):
        imagename, image_extension = os.path.splitext(self.imagename)
        return image_extension


class ModelDisplay(models.Model):
    display = models.CharField(_.f_display, blank=True, max_length=255, null=True)
    FORCE_UPDATE_DISPLAY = False
    SHOW_DISPLAY_IN_URL = True

    class Meta:
        abstract = True

    def set_display(self):
        if self.FORCE_UPDATE_DISPLAY or self.display is None and test(self.__str__()):
            self.display = str(self.__str__())

    def save(self, *args, **kwargs):
        self.set_display()
        super().save(*args, **kwargs)

class ModelToSearch(models.Model):
    to_search = models.TextField(_.f_to_search, db_index=True, blank=True, null=True)

    class Meta:
        abstract = True

    def set_to_search(self):
        self.to_search = make_searchable(str(self.__str__()))

    def save(self, *args, **kwargs):
        self.set_to_search()
        super().save(*args, **kwargs)


class ModelSignHash(models.Model):
    signhash = models.CharField(_.f_signhash, db_index=True, blank=True, editable=False, max_length=254, null=True, unique=True)
    GENERATE_SIGNHASH = True

    class Meta:
        abstract = True

    def validate_unique(self, exclude=None):
        self.set_signhash()
        super().validate_unique(exclude)

    def get_signhash(self, *args, **kwargs):
        if self.GENERATE_SIGNHASH:
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
                    if hasattr(self, field.name):
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

    @property
    def enable_url(self):
        kwargs = {'uid': str(self.uid)} if hasattr(self, 'uid') else {'pk': str(self.pk)}
        if self.SHOW_DISPLAY_IN_URL: kwargs['display'] = quote_plus(self.display)
        return self.get_url('enable', kwargs=kwargs)
    
    @property
    def disable_url(self):
        kwargs = {'uid': str(self.uid)} if hasattr(self, 'uid') else {'pk': str(self.pk)}
        if self.SHOW_DISPLAY_IN_URL: kwargs['display'] = quote_plus(self.display)
        return self.get_url('disable', kwargs=kwargs)

    @property
    def enable_url_html(self):
        return self.get_url_html('enable', self.title['enable'])

    @property
    def disable_url_html(self):
        return self.get_url_html('disable', self.title['disable'])

class ModelAlert(models.Model):
    alerts = JSONField(_.f_alerts, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def is_in_alert(self):
        return True if alert is not None else False

    @property
    def title(self):
        title = super().title
        t_inalert = _('Est en alerte')
        title.update({'in_alert': _.t_inalert})
        return title


class ModelError(models.Model):
    errors = JSONField(_.f_errors, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def is_in_error(self):
        return True if error is not None else False

    @property
    def title(self):
        title = super().title
        title.update({'in_error': _.t_inerror})
        return title

class ModelPermissions(models.Model):
    CAN_ASK_FOR_PERMISSIONS = True

    def perm(self, perm):
        return '%s.%s_%s' % (str(self.app_label).lower(), perm, str(self.model_name).lower())

    class Meta:
        abstract = True

class ModelSource(models.Model):
    sources = JSONField(_.f_sources, blank=True, null=True)

    class Meta:
        abstract = True

    def add_source(self, field, source, save=False):
        self.source[field] = source
        if save: self.save()

    def delete_source(self, field, save=False):
        del self.source[field]
        if save: self.save()

class ModelFile(ModelBase, ModelUid):
    the_file = models.FileField(upload_to=file_directory_path)
    mimetype = models.CharField(_.f_mimetype, max_length=255, blank=True, null=True)
    file_name = models.CharField(_.f_file_name, max_length=255, blank=True, null=True)
    
    class Meta(ModelBase.Meta):
        abstract = True

    def get_mime_type(self):
        return mimetypes.guess_type()[1]

    @property
    def filename(self):
        return os.path.basename(self.the_file.name)

    @property
    def valid_filename(self):
        return get_valid_filename(self.filename)

    @property
    def file_extension(self):
        filename, file_extension = os.path.splitext(self.filename)
        return file_extension

    @property
    def fonta(self):
        return "alt"

    @property
    def url(self):
        return self.the_file.url

    def save(self, *args, **kwargs):
        if self.file_name is None:
            self.file_name = self.valid_filename
        super().save(*args, **kwargs)

class ModelFull(
    ModelUid,
    ModelBase,
    ModelDisable,
    ModelError,
    ModelAlert,
    ModelToSearch,
    ModelSignHash,
    ModelImage,
    ModelDisplay,
    ModelPermissions):
    class Meta(ModelBase.Meta):
        abstract = True