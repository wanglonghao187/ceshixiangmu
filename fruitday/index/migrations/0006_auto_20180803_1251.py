# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-08-03 04:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_goods_goodstype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'verbose_name': '商品', 'verbose_name_plural': '商品'},
        ),
        migrations.AlterModelOptions(
            name='goodstype',
            options={'verbose_name': '商品类型', 'verbose_name_plural': '商品类型'},
        ),
    ]