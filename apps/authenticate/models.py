from django.db import models
from django.contrib.auth import get_user_model
from mighty.models import JSONField
from mighty.models.abstracts import ModelBase, ModelPermissions
from mighty.apps.authenticate import translations as _

UserModel = get_user_model()

STATUS_PREPARE = 'PREPARE'
STATUS_SENT = 'SENT'
STATUS_RECEIVED = 'RECEIVED'

class Template(ModelBase, ModelPermissions):
    choices = ((STATUS_PREPARE, _.c_status_prepare), (STATUS_SENT, _.c_status_sent), (STATUS_RECEIVED, _.c_status_received),)
    status = models.CharField(_.f_status, choices=choices, default=STATUS_PREPARE, max_length=100, editable=False, help_text='<a href="check">%s</a>' % _.ht_status)
    backend = models.CharField(_.f_backend, max_length=255, editable=False)
    response = models.TextField(_.f_response, editable=False)
    
    class Meta(ModelBase.Meta):
        abstract = True

    def __str__(self):
        return "%s - %s" % (self.user, self.status)

    def get_backend(self):
        from django.utils.module_loading import import_string
        backend = import_string(self.backend)()
        return backend

class Email(Template):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='email_sendto_user', editable=False)
    subject = models.CharField(_.f_subject, max_length=255, editable=False)
    html = models.TextField(_.f_html, editable=False)
    txt = models.TextField(_.f_txt, editable=False)

    class Meta(Template.Meta):
        abstract = True
        verbose_name = _.v_email
        verbose_name_plural = _.vp_email

    def check_status(self):
        backend = self.get_backend()
        return backend.check_email(self)

class Sms(Template):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='sms_sendto_user', editable=False)
    sms = models.TextField(_.f_sms, editable=False)
    
    class Meta(Template.Meta):
        abstract = True
        verbose_name = _.v_sms
        verbose_name_plural = _.vp_sms

    def check_status(self):
        backend = self.get_backend()
        return backend.check_sms(self)
