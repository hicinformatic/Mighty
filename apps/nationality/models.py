from django.db import models
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html
from mighty.models.abstracts import ModelBase, ModelToSearch, ModelSignHash, ModelDisable, ModelPermissions
from mighty.apps.nationality import _

class Nationality(ModelBase, ModelToSearch, ModelSignHash, ModelDisable, ModelPermissions):
    country = models.CharField(_.f_country, max_length=255)
    alpha2 = models.CharField(_.f_alpha2, max_length=2)
    alpha3 = models.CharField(_.f_alpha3, max_length=3, blank=True, null=True)
    numeric = models.CharField(_.f_numeric, max_length=3, blank=True, null=True)
    GENERATE_SIGNHASH = True

    class Meta(ModelPermissions.Meta):
        abstract = True
        verbose_name = _.v_nationality
        verbose_name_plural = _.vp_nationality
        ordering = ['country', ]

    def __str__(self):
        return "%s (%s, %s, %s)" % (self.country, self.alpha2, self.alpha3, self.numeric)

    @property
    def image_url(self):
        return static('flags/%s.png' % self.alpha2.lower())

    def image_html(self):
        return format_html('<img src="%s" title="%s">' % (self.image_url, self.__str__()))
    image_html.short_description = _.f_flag
