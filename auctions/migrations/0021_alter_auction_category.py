# Generated by Django 4.0.6 on 2022-07-28 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_alter_auction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(blank=True, choices=[('Automotive', 'Automotive'), ('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('Home', 'Home'), ('Other', 'Other'), ('Toys', 'Toys')], max_length=20, null=True),
        ),
    ]
