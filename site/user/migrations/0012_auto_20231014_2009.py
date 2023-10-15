# Generated by Django 3.1.4 on 2023-10-14 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_userdoor_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdoor',
            name='full_name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nome Completo'),
        ),
        migrations.AlterField(
            model_name='userdoor',
            name='nickname',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Apelido'),
        ),
    ]