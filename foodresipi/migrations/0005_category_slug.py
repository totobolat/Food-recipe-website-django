# Generated by Django 5.0.1 on 2024-02-01 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodresipi', '0004_resipi_avg_rating_resipi_number_of_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]