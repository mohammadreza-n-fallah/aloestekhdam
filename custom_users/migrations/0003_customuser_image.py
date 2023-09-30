# Generated by Django 4.2.5 on 2023-09-30 11:11

import custom_users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0002_state_customuser_balance_customuser_brand_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.FileField(blank=True, upload_to=custom_users.models.image_upload_to),
        ),
    ]
