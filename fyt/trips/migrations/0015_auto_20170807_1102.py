# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-07 15:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0014_triptype_hidden'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='dropoff_time',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='pickup_time',
        ),
    ]
