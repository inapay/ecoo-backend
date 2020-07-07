# Generated by Django 2.2.13 on 2020-07-07 13:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationInput',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=32)),
                ('data_type', models.IntegerField(choices=[(1, 'Text'), (2, 'Boolean'), (3, 'Date'), (4, 'Number')], default=0)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='currency.Currency')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
