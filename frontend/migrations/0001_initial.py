# Generated by Django 3.1.4 on 2021-02-13 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left_views', models.IntegerField(default=0)),
                ('viewed', models.IntegerField(default=0)),
                ('site_balance', models.FloatField(default=0.0, max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='PlansPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
                ('price_in_dollor', models.FloatField(default=0.0)),
                ('per_hour', models.FloatField(default=0.0)),
                ('per_day', models.FloatField(default=0.0)),
                ('per_month', models.FloatField(default=0.0)),
                ('life_time', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('code', models.CharField(blank=True, max_length=6, unique=True)),
                ('balance', models.FloatField(default=0.0, max_length=7)),
                ('purchase_balance', models.FloatField(default=0.0, max_length=7)),
                ('click', models.IntegerField(default=0)),
                ('per_hour', models.FloatField(default=0.0, max_length=7)),
                ('profit', models.FloatField(default=0.0, max_length=7)),
                ('alltime_earning', models.FloatField(default=0.0)),
                ('investment_plans', models.TextField(blank=True, null=True)),
                ('all_deposits', models.FloatField(default=0.0, max_length=7)),
                ('earned_click', models.FloatField(default=0.0, max_length=7)),
                ('deposit', models.FloatField(default=0.0, max_length=7)),
                ('paid_out', models.FloatField(default=0.0, max_length=7)),
                ('payeer', models.CharField(blank=True, max_length=9, null=True, unique=True)),
                ('perfectmoney', models.CharField(blank=True, max_length=9, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('plan_created', models.DateTimeField(auto_now_add=True)),
                ('no_plan', models.IntegerField(default=0)),
                ('no_ad', models.IntegerField(default=0)),
                ('title', models.CharField(blank=True, max_length=70, null=True)),
                ('url', models.URLField(blank=True)),
                ('ads', models.TextField(blank=True, null=True)),
                ('plans', models.TextField(blank=True, null=True)),
                ('recommended_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ref_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
