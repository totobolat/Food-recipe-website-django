# Generated by Django 5.0.1 on 2024-01-27 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodresipi', '0002_rename_resipiimages_resipiimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resipiimage',
            name='resipi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='foodresipi.resipi'),
        ),
    ]
