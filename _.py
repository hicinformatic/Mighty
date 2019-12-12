from django.utils.translation import gettext_lazy as _

site_header = _('Django administration (extend with Mighty)')
index_title = _('Site administration')
login = _('login')

cannotdisable = _("Cannot disable %(name)s")
disableok = _('The %(name)s "%(obj)s" was disabled successfully.')
cannotenable = _("Cannot enable %(name)s")
enableok = _('The %(name)s "%(obj)s" was enabled successfully.')
areyousure = _("Are you sure?")

f_display = _("Nom par défaut de l'objet")
f_to_search = _("Champs dédié à la recherche")
f_date_create = _("Date de création")
f_date_update = _("Date de mise à jour")
f_update_by = _("Mis à jour par")
f_is_disable = _("Objet désactivé")
f_signhash = _("Hash Signature")
f_initials = _("Initiales")
f_alerts = _('Alertes')
f_errors = _('Erreurs')
f_default = _('Défaut')
f_infos = _('Informations')
f_sources = _('Sources')
f_mimetype = _('Mime Type')
f_file_name = _('File name')

t_add  = _('Ajouter')
t_list  = _('Liste')
t_detail  = _('Détail')
t_change  = _('Modifier')
t_delete  = _('Supprimer')
t_enable  = _('Activer')
t_disable = _('Désactiver')
t_export = _("Exporter")
t_import = _("importer")
t_alert = _("Peut administrer les alertes")
t_error = _("Peut administrer les erreurs")
t_admin_perm = _("Peut administrer les permissions")
t_askfor_perm = _("Peut demander la permission d'un objet")
t_inalert = _('Est en alerte')
t_inerror = _('Est en erreur')
t_add_perm = _('Ajouter une permission')
t_remove_perm = _('Supprimer une permission')

p_can_view = _('Can view')
p_can_add = _('Can add')
p_can_change = _('Can change')
p_can_delete = _('Can delete')
p_can_enable = _('Can enable')
p_can_disable = _('Can disable')
p_can_add_perm = _('Can add permission')
p_can_remove_perm = _('Can remove permission')
p_can_view_perm = _('Can view permission')
p_can_change_perm = _('Can change permission')
p_can_askfor_perm = _('Can ask for permission')

e_emergency = _("urgence")
e_alert =  _("alerte")
e_critical = _("Critique")
e_error = _("erreur")
e_warning = _("attention")
e_notice = _("remarque")
e_info = _("informatif")
e_debug = _("débogue")
e_jsonfield = _("'%s' is not a valid JSON string.")
e_signhash = _("""La signature de l'objet ne peut être dupliqué, un objet similaire existe déjà""")
e_unique_perm = _("Vous faites déjà l'objet d'une demande concernant cette permission")

a_infos = _("Informations")

tpl_disable  = _("Are you sure you want to disable")
tpl_enable  = _("Are you sure you want to enable")
tpl_delete  = _("Are you sure you want to delete")
tpl_home = _("Accueil")
tpl_login = _("Connexion")
tpl_logout = _("Déconnexion")
tpl_admin = _("Admin")
tpl_admin_view = _("Vue d'administration")
tpl_clear = _("Effacer")