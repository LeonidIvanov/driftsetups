# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 21:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0010_auto_20171126_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carmodel',
            name='setups',
        ),
        migrations.RemoveField(
            model_name='carsubmodel',
            name='setups',
        ),
    ]
