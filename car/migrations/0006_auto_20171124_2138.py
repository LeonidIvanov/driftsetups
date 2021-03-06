# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 21:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('car', '0005_engine_producer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engine',
            name='stock_cars',
        ),
        migrations.AddField(
            model_name='engine',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='object_id',
            field=models.PositiveIntegerField(),
            preserve_default=False,
        ),
    ]
