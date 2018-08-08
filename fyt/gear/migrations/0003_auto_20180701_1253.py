# Generated by Django 2.0.6 on 2018-07-01 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('applications', '0116_auto_20180416_1613'),
        ('incoming', '0035_auto_20180412_1932'),
        ('gear', '0002_auto_20180628_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gearrequest',
            name='gear',
            field=models.ManyToManyField(blank=True, to='gear.Gear'),
        ),
        migrations.AlterUniqueTogether(
            name='gearrequest',
            unique_together={('trips_year', 'incoming_student'), ('trips_year', 'volunteer')},
        ),
    ]