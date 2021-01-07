# Generated by Django 3.1.4 on 2021-01-07 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='maxBid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='maxBid_rev', to='auctions.bid'),
        ),
    ]
