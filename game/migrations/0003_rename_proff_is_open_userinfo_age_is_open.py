# Generated by Django 5.1.5 on 2025-06-19 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0002_userinfo_fact_is_open_userinfo_health_is_open_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userinfo",
            old_name="proff_is_open",
            new_name="age_is_open",
        ),
    ]
