# Generated by Django 4.1.5 on 2023-01-26 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_coments', to=settings.AUTH_USER_MODEL)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blo_comgents', to='blog.blog', verbose_name='Blog')),
                ('likes', models.ManyToManyField(blank=True, related_name='likes_coments', to=settings.AUTH_USER_MODEL)),
                ('one_coments', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_one_coments', to='coment.coments')),
                ('tow_coments', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_tow_coments', to='coment.coments')),
                ('unlikes', models.ManyToManyField(blank=True, related_name='unlikes_coments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
