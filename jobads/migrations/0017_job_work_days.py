# Generated by Django 4.2.5 on 2023-09-25 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0016_remove_job_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='work_days',
            field=models.CharField(default='1', max_length=250),
            preserve_default=False,
        ),
    ]
