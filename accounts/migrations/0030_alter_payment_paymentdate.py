# Generated by Django 3.2 on 2021-04-15 06:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_alter_payment_paymentdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paymentDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 15, 12, 27, 17, 19073)),
        ),
    ]