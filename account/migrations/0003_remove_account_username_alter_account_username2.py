# Generated by Django 4.0 on 2024-04-17 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_username2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='username',
        ),
        migrations.AlterField(
            model_name='account',
            name='username2',
            field=models.CharField(max_length=60),
        ),
    ]
