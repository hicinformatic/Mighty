from django.db import models
from django.contrib.auth.models import AbstractUser

from mighty.models import JSONField
from mighty.models.abstracts import ModelFull
from mighty.functions import key, randomcode

from mighty.apps.user import _, fields
from mighty.apps.user.apps import UserConfig as conf
from mighty.apps.user.manager import UserManager

import time

class Nationality(ModelFull):
    country = models.CharField(_.f_country, max_length=255)
    alpha2 = models.CharField(_.f_alpha2, max_length=2)
    alpha3 = models.CharField(_.f_alpha3, max_length=3, blank=True, null=True)
    numeric = models.CharField(_.f_numeric, max_length=3, blank=True, null=True)
    GENERATE_SIGNHASH = True

    class Meta(ModelFull.Meta):
        abstract = True
        verbose_name = _.v_nationality
        verbose_name_plural = _.vp_nationality
        ordering = ['country', ]

    def __str__(self):
        return "%s (%s, %s, %s)" % (self.country, self.alpha2, self.alpha3, self.numeric)

    @property
    def image_url(self):
        return static('flags/%s.png' % self.alpha2.lower())

    @property
    def html(self):
        return format_html('<img src="%s" title="%s">' % (self.image_url, self.__str__()))

METHOD_CREATESU = 'CREATESUPERUSER'
METHOD_BACKEND = 'BACKEND'
METHOD_FRONTEND = 'FRONTEND'
METHOD_IMPORT = 'IMPORT'
GENDER_MAN = 'M'
GENDER_WOMAN = 'W'
class User(AbstractUser, ModelFull):
    username = models.CharField(_.f_username, max_length=254, validators=[AbstractUser.username_validator], unique=True, blank=True, null=True)
    email = models.EmailField(_.f_mail, unique=True, blank=True, null=True)
    choices = (
        (METHOD_CREATESU, _.c_method_createsuperuser),
        (METHOD_BACKEND, _.c_method_backend),
        (METHOD_FRONTEND, _.c_method_frontend),
        (METHOD_IMPORT, _.c_method_import),
    )
    method = models.CharField(_.f_method, choices=choices, default=METHOD_FRONTEND, max_length=15)
    sign = models.CharField(_.f_sign, default=key, max_length=32, unique=True, editable=False)
    key = models.CharField(_.f_key, default=key, max_length=32, unique=True, editable=False)
    choices = ((GENDER_MAN, _.c_man), (GENDER_WOMAN, _.c_woman))
    gender = models.CharField(_.f_gender, max_length=1, choices=choices, blank=True, null=True)
    phone = models.CharField(_.f_phone, blank=True, max_length=20, null=True, unique=True)
    tokens = JSONField(_.f_tokens, blank=True, null=True, editable=False)
    codes = JSONField(_.f_codes, blank=True, null=True, editable=False)
    ipv4 = models.GenericIPAddressField(_.f_ipv4, blank=True, null=True, editable=False)
    ipv6 = models.GenericIPAddressField(_.f_ipv6, blank=True, null=True, editable=False)

    USERNAME_FIELD = conf.Field.username
    REQUIRED_FIELDS = conf.Field.required
    URLFIELD_DISPLAY = ['username',]
    SHOW_DISPLAY_IN_URL = False
    objects = UserManager()

    class Meta(ModelFull.Meta):
        abstract = True
        verbose_name = _.v_user
        verbose_name_plural = _.vp_user
        ordering = ['last_name', 'first_name', 'email']

    def __str__(self):
        return getattr(self, self.USERNAME_FIELD)

    def set_signhash(self, *args, **kwargs):
        kwargs["notsignhash"] = fields.notsignhash
        signhash = self.get_signhash(*args, **kwargs)
        try:
            exist = self._meta.model.objects.get(signhash=signhash)
            if exist and exist.id != self.id:
                raise ValidationError(format_html(_.e_signhash % (exist.get_absolute_url, str(exist))))
        except self._meta.model.DoesNotExist:
            self.signhash = signhash

    def consume_code(self, code):
        if code in self.codes:
            del self.codes[code]
            self.save(update_fields=["codes"])
            return True
        return False

    def check_code(self, code):
        if code in self.codes:
            return True
        return False

    def add_code(self):
        code = randomcode(5)
        if self.codes is None:
            self.codes = {code: time.time()}
        else:
            self.codes[code] = time.time()
        self.save()
        return code

    def get_code(self):
        return next(iter(self.codes)) if len(self.codes) > 0 else self.add_code()

    def get_client_ip(self, request):
        self.ipv4 = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0] if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
        self.save()