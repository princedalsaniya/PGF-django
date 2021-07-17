# Generated by Django 3.1.7 on 2021-07-17 10:13

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
            name='Tenant',
            fields=[
                ('tenantID', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('workplace', models.CharField(max_length=500)),
                ('bdate', models.DateField()),
                ('isVarified', models.BooleanField(default=False)),
                ('profilePicID', models.CharField(max_length=200, unique=True)),
                ('adharNo', models.CharField(max_length=20, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('ownerID', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('isVarified', models.BooleanField(default=False)),
                ('profilePicID', models.CharField(max_length=200, unique=True)),
                ('adharNo', models.CharField(max_length=20, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
