# Generated by Django 3.1.1 on 2020-10-14 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20201015_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
