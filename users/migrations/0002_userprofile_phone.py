# Generated by Django 5.1.7 on 2025-05-19 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
