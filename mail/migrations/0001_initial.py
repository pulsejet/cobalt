# Generated by Django 2.0.5 on 2018-07-21 10:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BulkMail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time_of_creation', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('from_email', models.EmailField(max_length=254)),
                ('in_progress', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('template', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('data', models.TextField(blank=True)),
                ('sent', models.BooleanField(default=False)),
                ('failed', models.BooleanField(default=False)),
                ('bulk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mails', to='mail.BulkMail')),
            ],
        ),
    ]