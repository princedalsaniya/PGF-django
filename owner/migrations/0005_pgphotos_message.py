# Generated by Django 3.1.7 on 2021-07-23 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0004_auto_20210722_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='pgphotos',
            name='message',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
