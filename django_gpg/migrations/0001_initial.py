# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 14:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_gpg.fields


def add_profiles(apps, schema_editor):
    GpgProfile = apps.get_model('django_gpg', 'GpgProfile')
    User = apps.get_model(settings.AUTH_USER_MODEL)
    profiles = [GpgProfile(user=user) for user in User.objects.all()]
    db = schema_editor.connection.alias
    GpgProfile.objects.using(db).bulk_create(profiles)


def drop_profiles(apps, schema_editor):
    GpgProfile = apps.get_model('django_gpg', 'GpgProfile')
    db = schema_editor.connection.alias
    GpgProfile.objects.using(db).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='GpgProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('public_key', django_gpg.fields.PublicKeyField(validators=[django_gpg.fields.validate_public_key, django_gpg.fields.validate_public_key])),
            ],
            options={
                'verbose_name': 'GPG Profile',
            },
        ),
        migrations.RunPython(add_profiles, drop_profiles)
    ]