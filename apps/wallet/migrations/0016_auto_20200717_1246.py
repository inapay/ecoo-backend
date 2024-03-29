# Generated by Django 2.2.14 on 2020-07-17 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0015_auto_20200717_1002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallet',
            old_name='wallet_type',
            new_name='category',
        ),
        migrations.AddField(
            model_name='tokentransaction',
            name='nonce',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tokentransaction',
            name='operation_hash',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='tokentransaction',
            name='state',
            field=models.IntegerField(choices=[(1, 'Open'), (2, 'Pending'), (3, 'Done'), (4, 'Failed')], default=1),
        ),
    ]
