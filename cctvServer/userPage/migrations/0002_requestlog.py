# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-10 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userPage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('req', models.TextField()),
            ],
        ),
    ]
