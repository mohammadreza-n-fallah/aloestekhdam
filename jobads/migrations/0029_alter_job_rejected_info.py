# Generated by Django 4.2.5 on 2023-10-11 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0028_job_rejected_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='rejected_info',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
    ]
