# Generated by Django 4.1.7 on 2024-08-09 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DASH_pillars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicneedsupport',
            name='is_deactivated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='hardship',
            name='is_deactivated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='is_deactivated',
            field=models.BooleanField(default=False),
        ),
    ]
