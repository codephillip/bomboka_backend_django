# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-17 11:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0033_auto_20170816_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.Brand')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.Product')),
            ],
        ),
    ]
