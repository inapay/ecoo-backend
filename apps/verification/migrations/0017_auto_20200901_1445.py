# Generated by Django 3.1 on 2020-09-01 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0016_addresspinverification_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyverification',
            name='uid',
            field=models.CharField(max_length=15, null=True, verbose_name='Uid'),
        ),
    ]
