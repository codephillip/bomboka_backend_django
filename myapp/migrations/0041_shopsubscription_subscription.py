# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-17 17:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0040_shopsubscription_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopsubscription',
            name='subscription',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.Subscription'),
            preserve_default=False,
        ),
    ]
