# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-08 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0012_auto_20170808_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stoporder',
            name='computed_time',
            field=models.TimeField(default=None, editable=False, null=True, verbose_name='Pickup/dropoff time computed by Google Maps'),
        ),
    ]