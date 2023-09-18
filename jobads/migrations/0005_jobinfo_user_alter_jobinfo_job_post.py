# Generated by Django 4.2.5 on 2023-09-09 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobads', '0004_remove_jobinfo_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobinfo',
            name='user',
            field=models.ForeignKey(blank=True, null=True , on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jobinfo',
            name='job_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobinfo', to='jobads.job'),
        ),
    ]
