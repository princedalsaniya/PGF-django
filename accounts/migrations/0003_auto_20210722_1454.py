# Generated by Django 3.1.7 on 2021-07-22 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210717_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='profilePicID',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
