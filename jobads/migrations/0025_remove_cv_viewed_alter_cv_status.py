# Generated by Django 4.2.5 on 2023-10-09 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobads', '0024_cv_viewed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cv',
            name='viewed',
        ),
        migrations.AlterField(
            model_name='cv',
            name='status',
            field=models.CharField(default='unseen', max_length=250),
        ),
    ]
