# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-26 11:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_user_u_isdelete'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_num', models.IntegerField(default=1)),
                ('c_isselect', models.BooleanField(default=1)),
                ('c_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.goods')),
                ('c_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User')),
            ],
            options={
                'db_table': 'axf_cart',
            },
        ),
    ]
