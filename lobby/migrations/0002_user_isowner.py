# Generated by Django 5.1.5 on 2025-06-15 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lobby", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="isOwner",
            field=models.BooleanField(default=False),
        ),
    ]
