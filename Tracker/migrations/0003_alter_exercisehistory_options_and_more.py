# Generated by Django 5.2 on 2025-05-03 20:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Tracker", "0002_bodymetrics_exercise_meal"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exercisehistory",
            options={},
        ),
        migrations.AlterField(
            model_name="exercisehistory",
            name="duration",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="exercisehistory",
            name="exercise_name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="exercisehistory",
            name="exercise_type",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="exercisehistory",
            name="reps",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="exercisehistory",
            name="sets",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.CreateModel(
            name="MealHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("food_name", models.CharField(max_length=100)),
                ("calories", models.IntegerField()),
                ("protein", models.FloatField()),
                ("carbs", models.FloatField()),
                ("fat", models.FloatField()),
                ("fiber", models.FloatField()),
                ("sugar", models.FloatField()),
                ("sodium", models.FloatField()),
                ("notes", models.TextField(blank=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
