# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-28 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='length',
            field=models.CharField(default=0, max_length=100, verbose_name='\u89c6\u9891\u957f\u5ea6'),
        ),
    ]
