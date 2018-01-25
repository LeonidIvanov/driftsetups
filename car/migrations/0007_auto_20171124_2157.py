# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0006_auto_20171124_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engine',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='engine',
            name='object_id',
        ),
        migrations.AddField(
            model_name='engine',
            name='stock_cars',
            field=models.ManyToManyField(to='car.CarSubModel'),
        ),
    ]
