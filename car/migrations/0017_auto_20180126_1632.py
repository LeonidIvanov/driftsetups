# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-26 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0016_auto_20180123_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='stock_engines',
            field=models.ManyToManyField(blank=True, to='car.Engine'),
        ),
        migrations.AlterField(
            model_name='carsubmodel',
            name='stock_engines',
            field=models.ManyToManyField(blank=True, to='car.Engine'),
        ),
    ]
