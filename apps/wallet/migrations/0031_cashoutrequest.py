# Generated by Django 2.2.14 on 2020-08-06 09:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0030_auto_20200805_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashOutRequest',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('state', models.IntegerField(choices=[(1, 'Open'), (2, 'Pending'), (3, 'Done'), (4, 'Failed')], default=1)),
                ('beneficiary_name', models.CharField(max_length=255, verbose_name='Beneficiary name')),
                ('beneficiary_iban', models.CharField(max_length=255, verbose_name='IBAN')),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cash_out_requests', to='wallet.Transaction')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
