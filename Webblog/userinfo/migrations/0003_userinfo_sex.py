# Generated by Django 2.2 on 2019-04-26 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0002_auto_20190425_0512'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='sex',
            field=models.BooleanField(default=0),
        ),
    ]