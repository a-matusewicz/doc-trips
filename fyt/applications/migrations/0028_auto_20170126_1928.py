# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-27 00:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0027_auto_20170126_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='index',
            field=models.PositiveIntegerField(help_text='change this value to re-order the questions', unique=True, verbose_name='order'),
        ),
    ]
