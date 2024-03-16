# Generated by Django 4.2.11 on 2024-03-16 17:17

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
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('status', models.CharField(choices=[('PUBLISHED', 'Published'), ('HIDDEN', 'Hidden')], default='PUBLISHED', max_length=9, verbose_name='status')),
                ('place', models.CharField(max_length=255, verbose_name='place')),
                ('timestamp', models.DateTimeField(verbose_name='timestamp')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='updated_at')),
                ('attendees', models.ManyToManyField(blank=True, related_name='events', to=settings.AUTH_USER_MODEL)),
                ('organizer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='organizer')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
    ]