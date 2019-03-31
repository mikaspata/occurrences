# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-03-31 00:07
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Occurence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('geo_location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('author', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField()),
            ],
            options={
                'ordering': ('-modified_date',),
            },
        ),
        migrations.CreateModel(
            name='OccurenceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='OccurenceState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='occurence',
            name='occurence_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.OccurenceCategory'),
        ),
        migrations.AddField(
            model_name='occurence',
            name='occurence_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.OccurenceState'),
        ),
    ]
