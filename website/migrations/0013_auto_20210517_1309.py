# Generated by Django 3.1.7 on 2021-05-17 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_auto_20210511_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidclientlot',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Ставка'),
        ),
        migrations.AlterField(
            model_name='bidcompanylot',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Ставка'),
        ),
    ]
