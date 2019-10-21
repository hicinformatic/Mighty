from django.utils.translation import gettext_lazy as _

f_search = _("""Numéro de téléphone, email ou nom d'utilisateur""")
f_status = _("Statut du message")
f_backend = _('Backend utilisé')
f_response = _("Contenu de la réponse")
f_user = _("Utilisateur")
f_sms = _("SMS")
f_subject = _("Sujet")
f_html = _("HTML")
f_txt = _("Text")

c_status_prepare = _('Préparé')
c_status_sent = _('Envoyé')
c_status_received = _('Reçu')

s_sms = _("Recevoir un code par SMS")
s_email = _("Recevoir un code par Email")

e_invalid_search = _("Please enter a correct Email, Phone or Username. Note that both fields may be case-sensitive.")
e_invalid_method = _("Method invalid")
e_invalid_login = _("Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.")
e_inactive = _("This account is inactive.")
e_cant_send = _("Impossible d'envoyer un message")
e_method_not_allowed = _("Cette méthod d'authentification n'est pas autorisée")

tpl_subject = _("%s - Code de connexion")
tpl_html = _("Voici votre code de vérification personnel pour vous connecter au site %s est %s")
tpl_txt = _("Voici votre code de vérification personnel pour vous connecter au site %s est %s")
tpl_email_code = _("Entrez le code reçu par Email:")
tpl_sms_code = _("Entrez le code reçu par SMS:")
tpl_basic_code = _("Entez votre mot de passe:")

send_method = _("Authentification par")
send_basic = _("Authentification par mot de passe")
submit_code =_("Me connecter")

method_email = _("Email")
method_sms = _("SMS")
method_basic = _("Mot de passe")

t_authenticate = _("On se connait déjà?")

v_sms = _('SMS')
v_email = _('Email')

vp_sms = _('SMS')
vp_email = _('Emails')

ht_status = _('Vérifier le status')