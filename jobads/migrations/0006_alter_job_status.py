# Generated by Django 4.2.5 on 2023-10-07 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0005_alter_job_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(max_length=100),
        ),
    ]