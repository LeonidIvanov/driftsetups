# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-23 12:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0015_remove_carimage_setup'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carbrand',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='carmodel',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='carsubmodel',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='engine',
            options={'ordering': ['name']},
        ),
    ]
