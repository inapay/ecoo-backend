# Generated by Django 2.2.14 on 2020-08-05 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0028_auto_20200805_0822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='created',
        ),
    ]
