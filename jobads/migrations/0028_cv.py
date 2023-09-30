# Generated by Django 4.2.5 on 2023-09-30 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jobads.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobads', '0027_alter_job_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(blank=True, unique=True, upload_to=jobads.models.cv_upload_to)),
                ('status', models.CharField(default='sent', max_length=250)),
                ('jobad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobads.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
