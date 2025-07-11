# Generated by Django 5.1.5 on 2025-07-01 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0004_voiting"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voiting",
            name="count_of_voice",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="voiting",
            name="have_voted",
            field=models.BooleanField(default=False),
        ),
    ]
