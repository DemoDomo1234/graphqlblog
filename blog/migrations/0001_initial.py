# Generated by Django 4.1.3 on 2022-11-26 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('date', models.DateTimeField()),
                ('image', models.ImageField(upload_to='images')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_author', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('likes', models.ManyToManyField(blank=True, null=True, related_name='blog_likes', to=settings.AUTH_USER_MODEL, verbose_name='Likes')),
                ('saved', models.ManyToManyField(blank=True, null=True, related_name='blog_saved', to=settings.AUTH_USER_MODEL, verbose_name='Saved')),
            ],
        ),
    ]
