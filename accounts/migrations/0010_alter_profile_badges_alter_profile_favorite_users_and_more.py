# Generated by Django 4.0.5 on 2022-07-18 12:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200410_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='badges',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=16), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='profile',
            name='favorite_users',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='profile',
            name='group_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
    ]