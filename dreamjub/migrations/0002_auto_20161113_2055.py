# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dreamjub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='picture',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
