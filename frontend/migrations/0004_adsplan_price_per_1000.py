# Generated by Django 3.1.4 on 2021-03-12 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_remove_plansplan_newfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='adsplan',
            name='price_per_1000',
            field=models.IntegerField(default=0),
        ),
    ]
