# Generated by Django 3.1.7 on 2021-05-10 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20210509_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidcompanylot',
            name='bidder',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='website.client'),
        ),
        migrations.AlterField(
            model_name='bidcompanylot',
            name='lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.companylot'),
        ),
        migrations.AlterField(
            model_name='clientlot',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Створено'),
        ),
        migrations.AlterField(
            model_name='clientlot',
            name='date_end',
            field=models.DateTimeField(verbose_name='Завершується'),
        ),
        migrations.AlterField(
            model_name='clientlot',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активний'),
        ),
        migrations.AlterField(
            model_name='companylot',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Створено'),
        ),
        migrations.AlterField(
            model_name='companylot',
            name='date_end',
            field=models.DateTimeField(verbose_name='Завершується'),
        ),
        migrations.AlterField(
            model_name='companylot',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активний'),
        ),
    ]
