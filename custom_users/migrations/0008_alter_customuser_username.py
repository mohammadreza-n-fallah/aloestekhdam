# Generated by Django 4.2.5 on 2023-12-28 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0007_customuser_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=250, null=True, unique=True),
        ),
    ]
