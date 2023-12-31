# Generated by Django 4.2.7 on 2023-11-26 01:37

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, unique=True, verbose_name='Nome Completo')),
                ('user_type', models.PositiveSmallIntegerField()),
                ('authorization', models.BooleanField(default=True)),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
        ),
        migrations.CreateModel(
            name='UserSystem',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='userform.user')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Administrador')),
                ('is_analist', models.BooleanField(default=False, verbose_name='Analista')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário Sistema',
                'verbose_name_plural': 'Usuários Sistema',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='userform.user')),
                ('user_course', models.CharField(max_length=100, verbose_name='Curso')),
                ('institution_code', models.IntegerField(unique=True, verbose_name='Matrícula')),
                ('user_project', models.CharField(max_length=100, verbose_name='Projeto')),
            ],
            options={
                'verbose_name': 'Aluno',
                'verbose_name_plural': 'Alunos',
            },
        ),
        migrations.CreateModel(
            name='UserDoor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='userform.user')),
                ('nickname', models.CharField(blank=True, max_length=12, null=True, verbose_name='Apelido')),
                ('expiration_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Usuário Porta',
                'verbose_name_plural': 'Usuários Porta',
            },
        ),
        migrations.CreateModel(
            name='PunchCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('punch_in_time', models.DateTimeField()),
                ('punch_out_time', models.DateTimeField(blank=True, null=True)),
                ('reviw', models.BooleanField(default=False)),
                ('out', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userform.user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='userDoor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doorUser', to='userform.userdoor'),
        ),
        migrations.AddField(
            model_name='user',
            name='userStudent',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studentUser', to='userform.student'),
        ),
        migrations.AddField(
            model_name='user',
            name='userSystem',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='systemUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='student',
            name='user_coordinator',
            field=models.ForeignKey(limit_choices_to={'user_type': 2}, on_delete=django.db.models.deletion.PROTECT, related_name='coordinator', to='userform.user'),
        ),
        migrations.CreateModel(
            name='Rfid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfid_uid', models.CharField(max_length=8, unique=True)),
                ('authorization', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userform.userdoor')),
            ],
        ),
    ]
