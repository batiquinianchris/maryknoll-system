# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-26 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrative', '0002_auto_20180209_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='password',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='username',
        ),
        migrations.AddField(
            model_name='employee',
            name='work_type',
            field=models.CharField(choices=[('f', 'Full Time'), ('p', 'Part Time'), ('n', 'Others')], default='n', max_length=1),
        ),
    ]