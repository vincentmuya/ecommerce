# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-31 07:22
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_image', models.ImageField(blank=True, null=True, upload_to='posts/')),
                ('item_description', tinymce.models.HTMLField()),
            ],
        ),
    ]
