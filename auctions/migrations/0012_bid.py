# Generated by Django 4.0.6 on 2022-07-27 00:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_watchlist_auctions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_value', models.DecimalField(decimal_places=2, max_digits=19, null='False')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_listing', to='auctions.auction')),
                ('user_bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_made_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
