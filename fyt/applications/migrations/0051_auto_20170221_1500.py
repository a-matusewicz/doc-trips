# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-21 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0050_auto_20170221_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalapplication',
            name='tshirt_size',
            field=models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Extra Extra Large')], max_length=3),
        ),
    ]