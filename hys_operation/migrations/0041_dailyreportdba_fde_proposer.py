# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-01-10 08:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hys_operation', '0040_auto_20180110_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyreportdba',
            name='fde_proposer',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, related_name='fpr', to='hys_operation.CoDicData', verbose_name='申请人(非开发)'),
            preserve_default=False,
        ),
    ]
