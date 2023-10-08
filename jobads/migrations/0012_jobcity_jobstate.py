# Generated by Django 4.2.5 on 2023-10-08 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0011_job_military_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=250, unique=True)),
            ],
        ),
    ]
