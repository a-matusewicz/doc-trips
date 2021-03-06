# Generated by Django 2.0.2 on 2018-03-04 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0075_auto_20180304_0850'),
    ]

    operations = [
        migrations.RenameField(
            model_name='volunteer',
            old_name='what_do_you_like_to_study',
            new_name='academic_interests',
        ),
        migrations.AlterField(
            model_name='leadersupplement',
            name='availability',
            field=models.TextField(blank=True, verbose_name="Looking at the Trips descriptions, please feel free to use this space to address any concerns or explain your availability. (Attention '20s: If you are available for more than Sections H, I, and J, please explain how.) If applicable, please also elaborate on any particular trips or activities that you absolutely CANNOT participate in. All information in this application will remain confidential."),
        ),
    ]
