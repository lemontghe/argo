# Generated by Django 3.1.4 on 2021-02-09 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='llleft_views',
            field=models.IntegerField(default=0),
        ),
    ]
