# Generated by Django 4.0.6 on 2022-07-28 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auction_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
