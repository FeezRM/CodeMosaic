# Generated by Django 5.1 on 2025-03-25 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_id",
            field=models.IntegerField(unique=True),
        ),
    ]
