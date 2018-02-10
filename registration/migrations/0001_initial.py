# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-10 02:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enrollment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drop',
            fields=[
                ('drop_ID', models.AutoField(primary_key=True, serialize=False)),
                ('drop_date', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('reason', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=2)),
                ('approved_date', models.DateTimeField(blank=True, null=True)),
                ('curriculum', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='enrollment.Curriculum')),
            ],
            options={
                'verbose_name': 'Drop',
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('enrollment_ID', models.AutoField(primary_key=True, serialize=False)),
                ('date_enrolled', models.DateField(auto_now_add=True)),
                ('student_type', models.CharField(choices=[('p', 'Paid'), ('i', 'Incomplete'), ('n', 'Payment Not Made'), ('d', 'Dropped out')], default='n', max_length=1)),
                ('curriculum', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='enrollment.Curriculum')),
                ('scholarship', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='enrollment.Scholarship')),
                ('school_year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='enrollment.School_Year')),
            ],
            options={
                'verbose_name': 'Enrollment',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_ID', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(max_length=200)),
                ('student_level', models.CharField(choices=[('g', 'Grade School'), ('j', 'Junior High'), ('s', 'Senior High'), ('o', 'Others')], default='o', max_length=1)),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], default='o', max_length=1)),
                ('status', models.CharField(choices=[('a', 'Active'), ('i', 'Inactive')], default='i', max_length=1)),
                ('birthplace', models.CharField(max_length=200)),
                ('birthdate', models.DateField()),
                ('home_addr', models.CharField(max_length=200)),
                ('postal_addr', models.CharField(max_length=200)),
                ('m_firstname', models.CharField(max_length=200)),
                ('m_middlename', models.CharField(max_length=200)),
                ('m_lastname', models.CharField(max_length=200)),
                ('m_occcupation', models.CharField(max_length=200)),
                ('f_firstname', models.CharField(max_length=200)),
                ('f_middlename', models.CharField(max_length=200)),
                ('f_lastname', models.CharField(max_length=200)),
                ('f_occupation', models.CharField(max_length=200)),
                ('guardian', models.CharField(max_length=200)),
                ('guardian_addr', models.CharField(max_length=200)),
                ('last_school', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['student_ID'],
            },
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='registration.Student'),
        ),
        migrations.AddField(
            model_name='drop',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.Student'),
        ),
    ]