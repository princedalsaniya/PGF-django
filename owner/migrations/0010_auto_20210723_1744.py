# Generated by Django 3.1.7 on 2021-07-23 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0009_auto_20210723_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pgapplication',
            name='pg',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='owner.pgdetails'),
        ),
    ]
