# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-18 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20170418_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='courseNums',
            field=models.IntegerField(default=0, verbose_name='\u8bfe\u7a0b\u6570'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='students',
            field=models.IntegerField(default=0, verbose_name='\u5b66\u4e60\u4eba\u6570'),
        ),
    ]
