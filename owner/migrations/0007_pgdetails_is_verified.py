# Generated by Django 3.1.7 on 2021-07-23 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0006_auto_20210723_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='pgdetails',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]