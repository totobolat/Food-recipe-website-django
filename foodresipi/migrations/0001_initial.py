# Generated by Django 5.0.1 on 2024-01-27 01:54

import django.core.validators
import django.db.models.deletion
import foodresipi.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=55)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=12, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('membership', models.CharField(choices=[('B', 'Lurker'), ('S', 'Creator'), ('G', 'Super Creator')], default='B', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='Resipi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=55)),
                ('description', models.TextField()),
                ('ingredients', models.TextField()),
                ('how_to', models.TextField()),
                ('slug', models.SlugField()),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='resipis', to='foodresipi.category')),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='foodresipi.chef')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ResipiImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='foodresipi/images', validators=[foodresipi.validators.validate_file_size])),
                ('resipi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodresipi.resipi')),
            ],
        ),
        migrations.CreateModel(
            name='ResipiRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodresipi.chef')),
                ('resipi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodresipi.resipi')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=55)),
                ('description', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('resipi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='foodresipi.resipi')),
            ],
        ),
    ]
