# Generated by Django 4.1 on 2022-09-01 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20220901_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.CharField(max_length=100),
        ),
    ]