# Generated by Django 4.0.6 on 2022-07-26 01:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auction_delete_auctions'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='user_post',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
