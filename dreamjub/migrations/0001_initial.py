# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 09:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LocalStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eid', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eid', models.IntegerField(unique=True)),
                ('active', models.BooleanField()),
                ('email', models.EmailField(max_length=254)),
                ('username', models.SlugField()),
                ('firstName', models.TextField(blank=True)),
                ('lastName', models.TextField(blank=True)),
                ('country', models.TextField(null=True)),
                ('picture', models.FileField(null=True, upload_to='')),
                ('college', models.CharField(choices=[('Krupp', 'Krupp College'), ('Mercator', 'Mercator College'), ('C3', 'College III'), ('Nordmetall', 'College Nordmetall')], max_length=255, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('isCampusPhone', models.BooleanField(default=False)),
                ('room', models.TextField(blank=True, null=True)),
                ('building', models.CharField(max_length=255, null=True)),
                ('isStudent', models.BooleanField()),
                ('isFaculty', models.BooleanField()),
                ('isStaff', models.BooleanField()),
                ('status', models.CharField(choices=[('foundation-year', 'Foundation Year'), ('undergrad', 'Undergraduate'), ('master', 'Master'), ('phd-integrated', 'integrated PhD'), ('phd', 'PhD'), ('winter', 'Winter School Student'), ('guest', 'Guest Student')], max_length=255, null=True)),
                ('degree', models.CharField(choices=[('Bachelor of Science', 'Bachelor of Science'), ('Bachelor of Art', 'Bachelor of Art'), ('Master of Science', 'Master of Science'), ('Master of Art', 'Master of Art'), ('PhD', 'PhD')], max_length=255, null=True)),
                ('year', models.PositiveIntegerField(null=True)),
                ('majorShort', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
