# Generated by Django 4.2.7 on 2023-11-26 00:15

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
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('full_name', models.CharField(max_length=100, unique=True, verbose_name='Nome Completo')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('user_type', models.PositiveSmallIntegerField()),
                ('is_admin', models.BooleanField(default=False, verbose_name='Administrador')),
                ('is_analist', models.BooleanField(default=False, verbose_name='Analista')),
                ('authorization', models.BooleanField(default=False, verbose_name='Autorização')),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserDoor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, unique=True, verbose_name='Nome Completo')),
                ('nickname', models.CharField(blank=True, max_length=12, null=True, verbose_name='Apelido')),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('isUser', models.BooleanField(default=True)),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
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
        migrations.CreateModel(
            name='PunchCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('punch_in_time', models.DateTimeField()),
                ('punch_out_time', models.DateTimeField(blank=True, null=True)),
                ('reviw', models.BooleanField(default=False)),
                ('out', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='doorUser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userform.userdoor'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user_course', models.CharField(max_length=100, verbose_name='Curso')),
                ('institution_code', models.IntegerField(unique=True, verbose_name='Matrícula')),
                ('user_project', models.CharField(max_length=100, verbose_name='Projeto')),
                ('user_coordinator', models.ForeignKey(limit_choices_to={'user_type': 2}, on_delete=django.db.models.deletion.CASCADE, related_name='coordinator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Aluno',
            },
        ),
    ]
