# Generated by Django 2.0.4 on 2018-04-12 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0106_auto_20180412_1227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leadersupplement',
            name='_old_available_sections',
        ),
        migrations.RemoveField(
            model_name='leadersupplement',
            name='_old_available_triptypes',
        ),
        migrations.RemoveField(
            model_name='leadersupplement',
            name='_old_preferred_sections',
        ),
        migrations.RemoveField(
            model_name='leadersupplement',
            name='_old_preferred_triptypes',
        ),
    ]