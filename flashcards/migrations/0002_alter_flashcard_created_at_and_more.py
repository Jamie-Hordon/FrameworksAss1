# Generated by Django 5.1.3 on 2024-12-07 00:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flashcards", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flashcard",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="flashcardset",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
