# Generated by Django 4.2.5 on 2023-09-05 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0003_remove_job_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobinfo',
            name='text',
        ),
    ]
