# Generated by Django 2.0.5 on 2018-07-21 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_auto_20180721_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulkmail',
            name='from_email',
            field=models.CharField(max_length=150),
        ),
    ]
