# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-26 21:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event_invites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventinvite',
            name='invite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites', to='event_invites.Invite'),
        ),
    ]
