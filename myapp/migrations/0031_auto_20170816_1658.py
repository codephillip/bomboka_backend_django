# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-16 16:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_auto_20170816_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='model',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='number_plate',
        ),
    ]