# Generated by Django 4.2.5 on 2023-10-08 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0014_alter_jobcity_char_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobcity',
            name='char_id',
        ),
        migrations.RemoveField(
            model_name='jobstate',
            name='char_id',
        ),
        migrations.AddField(
            model_name='jobcity',
            name='related_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobads.jobstate'),
        ),
    ]
