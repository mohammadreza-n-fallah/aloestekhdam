# Generated by Django 4.2.5 on 2023-10-08 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0018_remove_jobstate_related_city_jobcity_related_states'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcity',
            name='related_states',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='states', to='jobads.jobstate'),
        ),
    ]
