# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0007_auto_20171124_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engine',
            name='stock_cars',
        ),
        migrations.AddField(
            model_name='carmodel',
            name='stock_engines',
            field=models.ManyToManyField(to='car.Engine'),
        ),
        migrations.AddField(
            model_name='carsubmodel',
            name='stock_engines',
            field=models.ManyToManyField(to='car.Engine'),
        ),
    ]
