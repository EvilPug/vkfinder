# Generated by Django 3.0.4 on 2020-04-08 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='code',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
