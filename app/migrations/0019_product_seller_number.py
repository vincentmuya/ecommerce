# Generated by Django 2.0 on 2019-10-25 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20191018_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seller_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
