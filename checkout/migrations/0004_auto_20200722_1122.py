# Generated by Django 3.0.8 on 2020-07-22 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20200721_0346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkoutaddress',
            name='order_number',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ordered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ordered_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='start_date',
        ),
    ]