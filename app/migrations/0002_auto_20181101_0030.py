# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-31 21:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_description',
            field=models.TextField(max_length=1000),
        ),
    ]
