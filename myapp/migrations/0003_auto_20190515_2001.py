# Generated by Django 2.2.1 on 2019-05-16 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20190515_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.CharField(default='windsor', max_length=20),
        ),
        migrations.AlterField(
            model_name='client',
            name='company',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
