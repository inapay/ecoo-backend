# Generated by Django 2.2.13 on 2020-07-22 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0009_currency_starting_capital'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='max_claims',
            field=models.IntegerField(default=5),
        ),
    ]
