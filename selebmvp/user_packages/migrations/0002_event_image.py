# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-12 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_packages', '0001_squashed_0011_auto_20160802_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='event image'),
        ),
    ]
