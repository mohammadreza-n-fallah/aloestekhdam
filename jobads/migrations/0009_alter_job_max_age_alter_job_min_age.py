# Generated by Django 4.2.5 on 2023-10-07 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0008_alter_job_min_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='max_age',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='min_age',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]