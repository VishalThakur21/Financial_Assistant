# Generated by Django 3.1.1 on 2020-10-09 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_transaction_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='details',
            field=models.ForeignKey(choices=False, on_delete=django.db.models.deletion.CASCADE, to='api.detail', verbose_name='DETAILS'),
        ),
    ]
