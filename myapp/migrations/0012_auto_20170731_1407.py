# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-31 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20170731_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='createdAt',
            field=models.DateField(auto_created=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='modifiedAt',
            field=models.DateField(auto_created=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]