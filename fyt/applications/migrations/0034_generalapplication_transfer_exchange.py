# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-20 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0033_auto_20170220_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalapplication',
            name='transfer_exchange',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Are you a transfer or exchange student?'),
        ),
    ]