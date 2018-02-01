# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-01-10 07:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hys_operation', '0038_auto_20180110_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoDicData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dic_name', models.CharField(max_length=200, verbose_name='字典名称')),
                ('seq', models.IntegerField(verbose_name='顺序号')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hys_operation.CoDicType', verbose_name='字典类型')),
            ],
            options={
                'verbose_name_plural': '字典表',
                'verbose_name': '字典表',
                'db_table': 'co_dic_data',
            },
        ),
        migrations.CreateModel(
            name='DailyReportDba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(null=True, verbose_name='创建时间')),
                ('request', models.TextField(max_length=10000, verbose_name='需求')),
                ('scripts', models.TextField(max_length=10000, null=True, verbose_name='脚本')),
                ('is_complete', models.BooleanField(default=False, verbose_name='是否已完成')),
                ('remark', models.TextField(max_length=10000, null=True, verbose_name='备注')),
                ('db_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='server', to='hys_operation.CoDicData', verbose_name='DB服务器')),
                ('db_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='username', to='hys_operation.CoDicData', verbose_name='DB用户名')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oper', to='hys_operation.CoDicData', verbose_name='操作人')),
                ('proposer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pro', to='hys_operation.CoDicData', verbose_name='申请人')),
                ('request_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='re', to='hys_operation.CoDicData', verbose_name='需求类型')),
            ],
            options={
                'verbose_name_plural': 'DBA日志',
                'verbose_name': 'DBA日志',
                'db_table': 'daily_report_dba',
            },
        ),
    ]