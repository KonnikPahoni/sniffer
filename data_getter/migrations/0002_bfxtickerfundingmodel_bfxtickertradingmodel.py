# Generated by Django 3.1.8 on 2021-04-25 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_getter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BFXTickerFundingModel',
            fields=[
                ('gettermodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data_getter.gettermodel')),
                ('symbol', models.CharField(max_length=255)),
                ('frr', models.FloatField(blank=True, null=True)),
                ('bid', models.FloatField(blank=True, null=True)),
                ('bid_period', models.FloatField(blank=True, null=True)),
                ('bid_size', models.FloatField(blank=True, null=True)),
                ('ask', models.FloatField(blank=True, null=True)),
                ('ask_period', models.FloatField(blank=True, null=True)),
                ('ask_size', models.FloatField(blank=True, null=True)),
                ('daily_change', models.FloatField(blank=True, null=True)),
                ('daily_change_relative', models.FloatField(blank=True, null=True)),
                ('last_price', models.FloatField(blank=True, null=True)),
                ('volume', models.FloatField(blank=True, null=True)),
                ('high', models.FloatField(blank=True, null=True)),
                ('low', models.FloatField(blank=True, null=True)),
                ('frr_amount_available', models.FloatField(blank=True, null=True)),
            ],
            bases=('data_getter.gettermodel',),
        ),
        migrations.CreateModel(
            name='BFXTickerTradingModel',
            fields=[
                ('gettermodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data_getter.gettermodel')),
                ('symbol', models.CharField(max_length=255)),
                ('bid', models.FloatField(blank=True, null=True)),
                ('bid_size', models.FloatField(blank=True, null=True)),
                ('ask', models.FloatField(blank=True, null=True)),
                ('ask_size', models.FloatField(blank=True, null=True)),
                ('daily_change', models.FloatField(blank=True, null=True)),
                ('daily_change_relative', models.FloatField(blank=True, null=True)),
                ('last_price', models.FloatField(blank=True, null=True)),
                ('volume', models.FloatField(blank=True, null=True)),
                ('high', models.FloatField(blank=True, null=True)),
                ('low', models.FloatField(blank=True, null=True)),
            ],
            bases=('data_getter.gettermodel',),
        ),
    ]