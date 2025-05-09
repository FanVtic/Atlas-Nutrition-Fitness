# Generated by Django 5.2 on 2025-05-03 23:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Tracker", "0004_userprofile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="height_cm",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="height_feet",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="height_inches",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(11),
                ],
            ),
        ),
    ]
