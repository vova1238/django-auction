# Generated by Django 3.1.7 on 2021-05-08 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20210508_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientlot',
            name='price_gap',
            field=models.PositiveIntegerField(blank=True, default=30, help_text='(Ціна, на яку можуть змінювати ціну ставки)', verbose_name='Зміна ціни'),
        ),
        migrations.AlterField(
            model_name='companylot',
            name='price_gap',
            field=models.PositiveIntegerField(blank=True, default=30, help_text='(Ціна, на яку можуть змінювати ціну ставки)', verbose_name='Зміна ціни'),
        ),
    ]
