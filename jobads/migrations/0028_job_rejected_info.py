# Generated by Django 4.2.5 on 2023-10-11 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0027_cv_first_name_cv_job_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='rejected_info',
            field=models.CharField(default='', max_length=250),
        ),
    ]