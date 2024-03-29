# Generated by Django 2.2.14 on 2020-07-17 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0013_auto_20200716_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='is_company_wallet',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='is_owner_wallet',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='nonce',
        ),
        migrations.AddField(
            model_name='wallet',
            name='wallet_type',
            field=models.IntegerField(choices=[(0, 'Consumer'), (1, 'Company'), (2, 'Owner')], default=0),
        ),
        migrations.AlterField(
            model_name='tokentransaction',
            name='from_addr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='from_transactions', to='wallet.Wallet'),
        ),
        migrations.AlterField(
            model_name='tokentransaction',
            name='to_addr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='to_transactions', to='wallet.Wallet'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wallets', to='wallet.Company'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='wallets', to=settings.AUTH_USER_MODEL),
        ),
    ]
