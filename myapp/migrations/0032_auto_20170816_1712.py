# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-16 17:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0031_auto_20170816_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couriervehicle',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Vehicle', unique=True),
        ),
    ]