# Generated by Django 4.2.5 on 2023-10-07 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='max_age',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='min_age',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
