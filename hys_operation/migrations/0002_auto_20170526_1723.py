# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-26 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hys_operation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='user_mobile',
            field=models.BigIntegerField(),
        ),
    ]