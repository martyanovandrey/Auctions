# Generated by Django 3.1 on 2020-10-18 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0036_remove_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
