# Generated by Django 2.1.5 on 2019-02-14 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0126_auto_20190201_0802'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadersupplement',
            name='swim_test',
            field=models.NullBooleanField(choices=[(True, 'Yes'), (False, 'No')], default=None, verbose_name='Have you passed the Dartmouth swim test?'),
        ),
    ]
