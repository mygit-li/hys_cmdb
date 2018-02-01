# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-01-10 06:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hys_operation', '0036_auto_20180110_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='server',
        ),
        migrations.AddField(
            model_name='record',
            name='handle',
            field=models.CharField(default='', max_length=200, verbose_name='故障处理'),
        ),
        migrations.AlterField(
            model_name='record',
            name='trouble',
            field=models.CharField(max_length=200, verbose_name='故障内容'),
        ),
    ]
