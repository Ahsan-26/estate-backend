# Generated by Django 5.1.6 on 2025-02-24 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_inquiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='location',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
