# Generated by Django 3.1.1 on 2020-09-11 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeder', '0001_initial'),
        ('agprofile', '0003_auto_20200911_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agprofile',
            name='subscribe_to',
        ),
        migrations.AddField(
            model_name='agprofile',
            name='subscribe_to',
            field=models.ManyToManyField(to='feeder.SiteFeeder'),
        ),
    ]
