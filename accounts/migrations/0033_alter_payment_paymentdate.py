# Generated by Django 3.2 on 2021-04-16 10:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_auto_20210416_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paymentDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 16, 16, 31, 40, 481045)),
        ),
    ]
