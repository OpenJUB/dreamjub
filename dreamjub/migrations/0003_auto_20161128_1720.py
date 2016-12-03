# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 17:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dreamjub', '0002_auto_20161113_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('active', models.BooleanField()),
                ('cid', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseMemberships',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dreamjub.Course')),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='picture',
            field=models.ImageField(null=True, upload_to='faces/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='coursememberships',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dreamjub.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='coursememberships',
            unique_together=set([('course', 'student')]),
        ),
    ]
