# Generated by Django 5.0.1 on 2024-04-27 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("team", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="upcoming_matches",
        ),
    ]
