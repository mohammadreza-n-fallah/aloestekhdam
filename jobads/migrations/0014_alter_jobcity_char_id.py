# Generated by Django 4.2.5 on 2023-10-08 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0013_jobcity_char_id_jobstate_char_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcity',
            name='char_id',
            field=models.IntegerField(),
        ),
    ]