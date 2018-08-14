# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-07-24 02:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=20)),
                ('uphone', models.CharField(max_length=11)),
                ('uemail', models.EmailField(max_length=254)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
    ]
