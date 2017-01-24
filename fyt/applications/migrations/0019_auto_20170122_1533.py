# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-22 20:33
from __future__ import unicode_literals

from django.db import migrations

"""
Populate GeneralApplication.document with a placeholder document.
This lets the `application_complete` methods and queries continue
to work correctly.

We need to add handling to properly show the deprecated documents.
"""


def populate_document_field(apps, schema_editor):
    Application = apps.get_model('applications', 'GeneralApplication')

    for app in Application.objects.all():
        if app.leader_supplement.document or app.croo_supplement.document:
            app.document = (
                "Created before separate applications were deprecated."
            )
            app.save()


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0018_auto_20170122_1349'),
    ]

    operations = [
        migrations.RunPython(populate_document_field)
    ]
