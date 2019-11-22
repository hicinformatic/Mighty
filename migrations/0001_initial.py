# Generated by Django 2.2.7 on 2019-11-05 09:07

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mighty.apps.user.manager
import mighty.functions
import mighty.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('update_by', models.CharField(blank=True, editable=False, max_length=254, null=True, verbose_name='Mis à jour par')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('image', models.ImageField(blank=True, default='none.jpg', null=True, upload_to=mighty.functions.image_directory_path)),
                ('display', models.CharField(blank=True, max_length=255, null=True, verbose_name="Nom par défaut de l'objet")),
                ('to_search', models.TextField(blank=True, db_index=True, editable=False, null=True, verbose_name='Champs dédié à la recherche')),
                ('signhash', models.CharField(blank=True, db_index=True, editable=False, max_length=254, null=True, unique=True, verbose_name='Hash Signature')),
                ('is_disable', models.BooleanField(default=False, editable=False, verbose_name='Objet désactivé')),
                ('alerts', mighty.models.JSONField(blank=True, null=True, verbose_name='Alertes')),
                ('errors', mighty.models.JSONField(blank=True, null=True, verbose_name='Erreurs')),
                ('username', models.CharField(blank=True, max_length=254, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Identifiant')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='E-mail')),
                ('method', models.CharField(choices=[('CREATESUPERUSER', '.manage createsuperuser'), ('BACKEND', 'Back-end'), ('FRONTEND', 'Front-end'), ('IMPORT', 'Import (csv/xls)')], default='FRONTEND', max_length=15, verbose_name='Méthode')),
                ('sign', models.CharField(default=mighty.functions.key, editable=False, max_length=32, unique=True, verbose_name='Signature')),
                ('key', models.CharField(default=mighty.functions.key, editable=False, max_length=32, unique=True, verbose_name='Clé')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Homme'), ('W', 'Femme')], max_length=1, null=True, verbose_name='Genre')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Téléphone')),
                ('tokens', mighty.models.JSONField(blank=True, editable=False, null=True, verbose_name='Jetons')),
                ('codes', mighty.models.JSONField(blank=True, editable=False, null=True, verbose_name='Codes')),
                ('ipv4', models.GenericIPAddressField(blank=True, editable=False, null=True, verbose_name='IPv4')),
                ('ipv6', models.GenericIPAddressField(blank=True, editable=False, null=True, verbose_name='IPv6')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'Utilisateur',
                'verbose_name_plural': 'Utilisateurs',
                'ordering': ['last_name', 'first_name', 'email'],
                'abstract': False,
                'default_permissions': ('add', 'detail', 'list', 'change', 'delete', 'enable', 'disable', 'admin_perm', 'askfor_perm'),
            },
            managers=[
                ('objects', mighty.apps.user.manager.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('update_by', models.CharField(blank=True, editable=False, max_length=254, null=True, verbose_name='Mis à jour par')),
                ('image', models.ImageField(blank=True, default='none.jpg', null=True, upload_to=mighty.functions.image_directory_path)),
                ('to_search', models.TextField(blank=True, db_index=True, editable=False, null=True, verbose_name='Champs dédié à la recherche')),
                ('signhash', models.CharField(blank=True, db_index=True, editable=False, max_length=254, null=True, unique=True, verbose_name='Hash Signature')),
                ('is_disable', models.BooleanField(default=False, editable=False, verbose_name='Objet désactivé')),
                ('country', models.CharField(max_length=255, verbose_name='Pays')),
                ('alpha2', models.CharField(max_length=2, verbose_name='Alpha2')),
                ('alpha3', models.CharField(blank=True, max_length=3, null=True, verbose_name='alpha3')),
                ('numeric', models.CharField(blank=True, max_length=3, null=True, verbose_name='Numérique')),
            ],
            options={
                'verbose_name': 'Nationalité',
                'verbose_name_plural': 'Nationalités',
                'ordering': ['country'],
                'abstract': False,
                'default_permissions': ('add', 'detail', 'list', 'change', 'delete', 'enable', 'disable', 'admin_perm', 'askfor_perm'),
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('update_by', models.CharField(blank=True, editable=False, max_length=254, null=True, verbose_name='Mis à jour par')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('image', models.ImageField(blank=True, default='none.jpg', null=True, upload_to=mighty.functions.image_directory_path)),
                ('display', models.CharField(blank=True, max_length=255, null=True, verbose_name="Nom par défaut de l'objet")),
                ('to_search', models.TextField(blank=True, db_index=True, editable=False, null=True, verbose_name='Champs dédié à la recherche')),
                ('signhash', models.CharField(blank=True, db_index=True, editable=False, max_length=254, null=True, unique=True, verbose_name='Hash Signature')),
                ('is_disable', models.BooleanField(default=False, editable=False, verbose_name='Objet désactivé')),
                ('alerts', mighty.models.JSONField(blank=True, null=True, verbose_name='Alertes')),
                ('errors', mighty.models.JSONField(blank=True, null=True, verbose_name='Erreurs')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Nom')),
                ('graphtype', models.CharField(choices=[('BAR', 'Bar'), ('BIPOLAR', 'Bipolar'), ('FUNNEL', 'Funnel'), ('GAUGE', 'Gauge'), ('HORIZONTALBAR', 'Horizontal Bar'), ('HORIZONTALPROGRESSBARS', 'Horizontal Progress bars'), ('LINE', 'Line'), ('PIE', 'Pie'), ('RADAR', 'Radar'), ('ROSE', 'Rose'), ('SCATTER', 'Scatter'), ('SEMICIRCULARPROGRESSBARS', 'Semi-circular Progress bars'), ('VERTICALPROGRESSBARS', 'Vertical Progress bars'), ('WATERFALL', 'Waterfall'), ('DONUT', 'Donut'), ('GANTT', 'Gantt'), ('METER', 'Meter'), ('ODOMETER', 'Odometer'), ('RADIALSCATTER', 'Radial scatter'), ('THERMOMETER', 'Thermometer')], default='BAR', max_length=100, verbose_name='Type')),
                ('lg_width', models.PositiveSmallIntegerField(default=800, verbose_name='Large width')),
                ('lg_height', models.PositiveSmallIntegerField(default=400, verbose_name='Large height')),
                ('lg_max_width', models.PositiveSmallIntegerField(default=1200, verbose_name='Large max witdh')),
                ('lg_title_size', models.PositiveSmallIntegerField(default=18, verbose_name='Large title size')),
                ('lg_text_size', models.PositiveSmallIntegerField(default=14, verbose_name='Large text size')),
                ('lg_margin_inner', models.PositiveSmallIntegerField(default=25, verbose_name='Large margin inner')),
                ('md_width', models.PositiveSmallIntegerField(default=600, verbose_name='Medium width')),
                ('md_height', models.PositiveSmallIntegerField(default=300, verbose_name='Medium height')),
                ('md_max_width', models.PositiveSmallIntegerField(default=992, verbose_name='Medium max witdh')),
                ('md_title_size', models.PositiveSmallIntegerField(default=14, verbose_name='Medium title size')),
                ('md_text_size', models.PositiveSmallIntegerField(default=12, verbose_name='Medium text size')),
                ('md_margin_inner', models.PositiveSmallIntegerField(default=20, verbose_name='Medium margin inner')),
                ('sm_width', models.PositiveSmallIntegerField(default=400, verbose_name='Small width')),
                ('sm_height', models.PositiveSmallIntegerField(default=200, verbose_name='Small height')),
                ('sm_max_width', models.PositiveSmallIntegerField(default=768, verbose_name='Small max witdh')),
                ('sm_title_size', models.PositiveSmallIntegerField(default=12, verbose_name='Small title size')),
                ('sm_text_size', models.PositiveSmallIntegerField(default=10, verbose_name='Small text size')),
                ('sm_margin_inner', models.PositiveSmallIntegerField(default=10, verbose_name='Small margin inner')),
                ('options', mighty.models.JSONField(blank=True, null=True)),
                ('responsive_options', mighty.models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Graphic template',
                'verbose_name_plural': 'Graphic templates',
                'abstract': False,
                'default_permissions': ('add', 'detail', 'list', 'change', 'delete', 'enable', 'disable', 'admin_perm', 'askfor_perm'),
            },
        ),
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('update_by', models.CharField(blank=True, editable=False, max_length=254, null=True, verbose_name='Mis à jour par')),
                ('status', models.CharField(choices=[('PREPARE', 'Préparé'), ('SENT', 'Envoyé'), ('RECEIVED', 'Reçu')], default='PREPARE', editable=False, help_text='<a href="check">Vérifier le status</a>', max_length=100, verbose_name='Statut du message')),
                ('backend', models.CharField(editable=False, max_length=255, verbose_name='Backend utilisé')),
                ('response', models.TextField(editable=False, verbose_name='Contenu de la réponse')),
                ('sms', models.TextField(editable=False, verbose_name='SMS')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='sms_sendto_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SMS',
                'verbose_name_plural': 'SMS',
                'ordering': ['-date_create'],
                'permissions': [('check_sms', 'Can check SMS')],
                'abstract': False,
                'default_permissions': ('add', 'detail', 'list', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('update_by', models.CharField(blank=True, editable=False, max_length=254, null=True, verbose_name='Mis à jour par')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('image', models.ImageField(blank=True, default='none.jpg', null=True, upload_to=mighty.functions.image_directory_path)),
                ('display', models.CharField(blank=True, max_length=255, null=True, verbose_name="Nom par défaut de l'objet")),
                ('to_search', models.TextField(blank=True, db_index=True, editable=False, null=True, verbose_name='Champs dédié à la recherche')),
                ('signhash', models.CharField(blank=True, db_index=True, editable=False, max_length=254, null=True, unique=True, verbose_name='Hash Signature')),
                ('is_disable', models.BooleanField(default=False, editable=False, verbose_name='Objet désactivé')),
                ('alerts', mighty.models.JSONField(blank=True, null=True, verbose_name='Alertes')),
                ('errors', mighty.models.JSONField(blank=True, null=True, verbose_name='Erreurs')),
                ('title', models.CharField(max_length=255, verbose_name='Graphic title')),
                ('is_responsive', models.BooleanField(default=False, verbose_name='responsive')),
                ('svg_container', models.TextField(blank=True, null=True, verbose_name='Svg container HTML')),
                ('canvas_container', models.TextField(blank=True, null=True, verbose_name='Canvas container HTML')),
                ('width', models.PositiveSmallIntegerField(default=800, verbose_name='Width')),
                ('height', models.PositiveSmallIntegerField(default=400, verbose_name='Height')),
                ('max_width', models.PositiveSmallIntegerField(default=1200, verbose_name='Max witdh')),
                ('title_size', models.PositiveSmallIntegerField(default=18, verbose_name='Title size')),
                ('text_size', models.PositiveSmallIntegerField(default=14, verbose_name='Text size')),
                ('margin_inner', models.PositiveSmallIntegerField(default=25, verbose_name='Margin inner')),
                ('options', mighty.models.JSONField(blank=True, null=True)),
                ('responsive_options', mighty.models.JSONField(blank=True, null=True)),
                ('bar_values', mighty.models.JSONField(blank=True, null=True)),
                ('bipolar_values', mighty.models.JSONField(blank=True, null=True)),
                ('funnel_values', mighty.models.JSONField(blank=True, null=True)),
                ('gauge_values', mighty.models.JSONField(blank=True, null=True)),
                ('horizontalbar_values', mighty.models.JSONField(blank=True, null=True)),
                ('horizontalprogressbars_values', mighty.models.JSONField(blank=True, null=True)),
                ('line_values', mighty.models.JSONField(blank=True, null=True)),
                ('pie_values', mighty.models.JSONField(blank=True, null=True)),
                ('radar_values', mighty.models.JSONField(blank=True, null=True)),
                ('rose_values', mighty.models.JSONField(blank=True, null=True)),
                ('scatter_values', mighty.models.JSONField(blank=True, null=True)),
                ('semicircularprogressbars_values', mighty.models.JSONField(blank=True, null=True)),
                ('verticalprogressbars_values', mighty.models.JSONField(blank=True, null=True)),
                ('waterfall_values', mighty.models.JSONField(blank=True, null=True)),
                ('donut_values', mighty.models.JSONField(blank=True, null=True)),
                ('gantt_values', mighty.models.JSONField(blank=True, null=True)),
                ('meter_values', mighty.models.JSONField(blank=True, null=True)),
                ('odometer_values', mighty.models.JSONField(blank=True, null=True)),
                ('radialscatter_values', mighty.models.JSONField(blank=True, null=True)),
                ('thermometer_values', mighty.models.JSONField(blank=True, null=True)),
                ('templates', models.ManyToManyField(to='mighty.Template')),
            ],
            options={
                'verbose_name': 'Graphic',
                'verbose_name_plural': 'Graphics',
                'abstract': False,
                'default_permissions': ('add', 'detail', 'list', 'change', 'delete', 'enable', 'disable', 'admin_perm', 'askfor_perm'),
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('update_by', models.CharField(blank=True, editable=False, max_length=254, null=True, verbose_name='Mis à jour par')),
                ('status', models.CharField(choices=[('PREPARE', 'Préparé'), ('SENT', 'Envoyé'), ('RECEIVED', 'Reçu')], default='PREPARE', editable=False, help_text='<a href="check">Vérifier le status</a>', max_length=100, verbose_name='Statut du message')),
                ('backend', models.CharField(editable=False, max_length=255, verbose_name='Backend utilisé')),
                ('response', models.TextField(editable=False, verbose_name='Contenu de la réponse')),
                ('subject', models.CharField(editable=False, max_length=255, verbose_name='Sujet')),
                ('html', models.TextField(editable=False, verbose_name='HTML')),
                ('txt', models.TextField(editable=False, verbose_name='Text')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='email_sendto_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emails',
                'ordering': ['-date_create'],
                'permissions': [('check_email', 'Can check Email')],
                'abstract': False,
                'default_permissions': ('add', 'detail', 'list', 'change', 'delete'),
            },
        ),
        migrations.AddField(
            model_name='user',
            name='nationalities',
            field=models.ManyToManyField(blank=True, to='mighty.Nationality'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='PermissionAsk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.BigIntegerField(blank=True, db_index=True, null=True)),
                ('cuid', models.UUIDField(blank=True, db_index=True, null=True)),
                ('status', models.CharField(choices=[('waiting', 'En attente'), ('validate', 'Validé'), ('invalidate', 'Invalidé')], default='waiting', max_length=20, verbose_name='Status')),
                ('ipv4', models.GenericIPAddressField(blank=True, editable=False, null=True, verbose_name='IPv4')),
                ('ipv6', models.GenericIPAddressField(blank=True, editable=False, null=True, verbose_name='IPv6')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_type_permissionask', to='contenttypes.ContentType')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permission_permissionask', to='auth.Permission')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_permissionask', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Permission demandée',
                'verbose_name_plural': 'Permissions demandées',
                'abstract': False,
                'unique_together': {('user', 'permission', 'content_type')},
            },
        ),
    ]