# Generated by Django 4.2.5 on 2023-10-08 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0019_alter_jobcity_related_states'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobcity',
            name='related_states',
        ),
        migrations.AddField(
            model_name='jobstate',
            name='related_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_city', to='jobads.jobcity'),
        ),
    ]
