# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-01 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20181101_1141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='title',
        ),
        migrations.AddField(
            model_name='category',
            name='categories',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
