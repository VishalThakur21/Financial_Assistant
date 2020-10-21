# Generated by Django 3.1.1 on 2020-10-14 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0015_auto_20201015_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique_for_month='date_created', verbose_name='USER'),
        ),
    ]