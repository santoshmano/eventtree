# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-10 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0007_auto_20160910_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorcateringservice',
            name='photos',
            field=models.ManyToManyField(to='vendors.VendorPhoto'),
        ),
    ]
