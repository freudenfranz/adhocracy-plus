# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liqd_product_cms_updates', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keepmeupdatedemail',
            name='interested_as_citizen',
            field=models.BooleanField(verbose_name='interested as citizen'),
        ),
        migrations.AlterField(
            model_name='keepmeupdatedemail',
            name='interested_as_municipality',
            field=models.BooleanField(verbose_name='interested as municipality'),
        ),
    ]
