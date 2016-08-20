# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-12 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_packages', '0002_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.CharField(blank=True, help_text='Enter the Image Filename', max_length=250, null=True, verbose_name='event image'),
        ),
    ]