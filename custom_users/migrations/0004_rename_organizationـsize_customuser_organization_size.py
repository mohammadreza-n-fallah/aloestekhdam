# Generated by Django 4.2.5 on 2023-09-05 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0003_customuser_organizationـsize'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='organizationـsize',
            new_name='organization_size',
        ),
    ]
