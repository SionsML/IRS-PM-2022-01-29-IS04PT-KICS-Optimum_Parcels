# Generated by Django 3.1.2 on 2022-04-22 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0003_remove_courier_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courier',
            name='estimatedDeliveryDuration',
        ),
        migrations.RemoveField(
            model_name='courier',
            name='homeDelivery',
        ),
        migrations.RemoveField(
            model_name='courier',
            name='insurance',
        ),
        migrations.RemoveField(
            model_name='courier',
            name='price',
        ),
        migrations.RemoveField(
            model_name='courier',
            name='reDelivery',
        ),
        migrations.RemoveField(
            model_name='courier',
            name='service',
        ),
        migrations.RemoveField(
            model_name='courier',
            name='serviceRating',
        ),
    ]
