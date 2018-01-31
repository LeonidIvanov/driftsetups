# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-30 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0016_auto_20180130_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='setupimage',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name='setupimage',
            options={'ordering': ['order']},
        ),
        migrations.RemoveField(
            model_name='setupimage',
            name='is_main',
        ),
    ]
