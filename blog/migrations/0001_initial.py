# Generated by Django 4.2.5 on 2023-09-05 10:53

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=250)),
                ('homepage', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250)),
                ('body', models.TextField()),
                ('publish', models.BooleanField(default=False)),
                ('admin_reply', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, unique=True)),
                ('description', models.TextField()),
                ('image', models.FileField(blank=True, upload_to='')),
                ('body', ckeditor.fields.RichTextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.CharField(max_length=500, unique=True)),
                ('category', models.ManyToManyField(to='blog.blogcategory')),
            ],
        ),
    ]
