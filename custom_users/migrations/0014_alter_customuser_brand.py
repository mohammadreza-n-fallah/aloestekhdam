# Generated by Django 4.2.5 on 2023-09-27 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0013_rename_companycity_city_customuser_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='brand',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
