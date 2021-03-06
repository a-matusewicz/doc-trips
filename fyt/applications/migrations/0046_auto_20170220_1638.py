# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-20 21:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0045_auto_20170220_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='croosupplement',
            name='kitchen_lead_qualifications',
            field=models.TextField(blank=True, help_text='(e.g. on Moosilauke Lodge crew spring 2014, experience working in industrial kitchens, experience preparing and organizing food for large groups)', verbose_name='If you are willing to be a Kitchen Magician, please briefly describe your qualifications for the position'),
        ),
        migrations.AlterField(
            model_name='croosupplement',
            name='kitchen_lead_willing',
            field=models.BooleanField(default=False, verbose_name='Yes, I am willing to be a Kitchen Magician'),
        ),
    ]
