# Generated by Django 2.0.4 on 2018-04-12 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incoming', '0034_auto_20180310_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='_old_available_sections',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='_old_available_triptypes',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='_old_firstchoice_triptype',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='_old_preferred_sections',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='_old_preferred_triptypes',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='_old_unavailable_sections',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='_old_unavailable_triptypes',
        ),
    ]
