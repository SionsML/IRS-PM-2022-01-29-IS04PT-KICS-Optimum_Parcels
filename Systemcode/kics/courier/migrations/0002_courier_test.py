# Generated by Django 3.1.2 on 2022-04-09 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courier',
            name='test',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]