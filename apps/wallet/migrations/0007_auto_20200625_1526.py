# Generated by Django 2.2.13 on 2020-06-25 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
        ('wallet', '0006_auto_20200625_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='currency',
        ),
        migrations.AddField(
            model_name='claimableamount',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='currency.Currency'),
        ),
    ]
