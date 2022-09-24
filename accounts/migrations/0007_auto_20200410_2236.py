# Generated by Django 3.0.4 on 2020-04-10 19:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200410_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='badges',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=16), blank=True, default=[], size=None),
            preserve_default=False,
        ),
    ]
