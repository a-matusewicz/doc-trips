# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-12 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_auto_20170412_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='sessions',
            field=models.ManyToManyField(blank=True, to='training.Session'),
        ),
    ]
