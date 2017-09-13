# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-12 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20170912_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='equality_on_offer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.IntegerField(choices=[(0, b'Pre-ICO'), (1, b'ICO')], default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='ratio',
            field=models.FloatField(default=1),
        ),
    ]
