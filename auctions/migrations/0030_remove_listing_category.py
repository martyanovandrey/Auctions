# Generated by Django 3.1 on 2020-10-18 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0029_auto_20201018_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
    ]