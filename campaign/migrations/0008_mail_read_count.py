# Generated by Django 2.1.5 on 2019-05-17 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0007_auto_20190517_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='read_count',
            field=models.IntegerField(default=0),
        ),
    ]
