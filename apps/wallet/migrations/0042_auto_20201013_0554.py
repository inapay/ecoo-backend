# Generated by Django 3.1 on 2020-10-13 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0041_auto_20200918_0626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metatransaction',
            name='signature',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='state',
            field=models.IntegerField(choices=[(0, 'Unverified'), (1, 'Pending'), (2, 'Verified'), (3, 'Deactivated')], default=0, verbose_name='State'),
        ),
    ]
