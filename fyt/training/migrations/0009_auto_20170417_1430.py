# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-17 18:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0008_auto_20170417_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='session',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
