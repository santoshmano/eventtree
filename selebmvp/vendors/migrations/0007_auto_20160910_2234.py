# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-10 20:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0006_auto_20160910_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorServicePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=250)),
                ('vendor_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='vendors.VendorService')),
            ],
        ),
        migrations.AddField(
            model_name='vendorlocationservice',
            name='photos',
            field=models.ManyToManyField(to='vendors.VendorPhoto'),
        ),
        migrations.AddField(
            model_name='vendorphoto',
            name='title',
            field=models.CharField(default=datetime.datetime(2016, 9, 10, 20, 34, 1, 995734, tzinfo=utc), max_length=250),
            preserve_default=False,
        ),
    ]