# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 09:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20160208_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpost',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Draft'), (1, 'Private'), (2, 'Published')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Draft'), (1, 'Private'), (2, 'Published')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='blog.Tag'),
        ),
    ]
