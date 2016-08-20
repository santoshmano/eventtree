# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-20 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_packages', '0003_auto_20160812_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(help_text='Enter the Event Name', max_length=250, verbose_name='event name'),
        ),
    ]