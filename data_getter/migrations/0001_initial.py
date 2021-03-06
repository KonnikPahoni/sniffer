# Generated by Django 3.1.4 on 2021-07-20 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BFXTickerFundingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, db_index=True, unique=True)),
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
        ),
        migrations.CreateModel(
            name='BFXTickerTradingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, db_index=True, unique=True)),
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
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField(db_index=True, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('roles_csv', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('registered', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdminSettings',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='data_getter.user')),
                ('logging_level', models.SmallIntegerField(default=30)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handler_name', models.CharField(max_length=255)),
                ('current_status', models.CharField(max_length=15)),
                ('interval', models.IntegerField()),
                ('last_update', models.DateTimeField(auto_now_add=True)),
                ('day_started', models.DateTimeField(auto_now_add=True)),
                ('public_name', models.CharField(max_length=255)),
                ('tags_csv', models.CharField(max_length=1000)),
                ('description', models.TextField()),
                ('image', models.FileField(upload_to='public/images/')),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_getter.user')),
            ],
        ),
    ]
