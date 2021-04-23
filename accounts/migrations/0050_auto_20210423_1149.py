# Generated by Django 3.2 on 2021-04-23 06:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0049_alter_payment_paymentdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='totalPrice',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paymentDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 23, 11, 49, 11, 428916)),
        ),
    ]
