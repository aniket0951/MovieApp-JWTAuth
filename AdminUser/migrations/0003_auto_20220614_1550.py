# Generated by Django 3.2.13 on 2022-06-14 15:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Merchent', '0003_seats'),
        ('AdminUser', '0002_movies_movie_langauge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='movie_release_date',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 6, 14, 15, 50, 4, 137559, tzinfo=utc), null=True),
        ),
        migrations.CreateModel(
            name='MovieAllocations',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movie', to='AdminUser.movies')),
                ('theter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='thetersinfo', to='Merchent.theterinformation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
