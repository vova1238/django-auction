# Generated by Django 3.1.7 on 2021-04-06 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clientlot',
            options={'verbose_name': 'Лот клієнта', 'verbose_name_plural': 'Лоти клієнтів'},
        ),
        migrations.AlterField(
            model_name='clientlot',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.client', verbose_name='Власник'),
        ),
        migrations.AlterField(
            model_name='clientreview',
            name='comment_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.company'),
        ),
        migrations.AlterField(
            model_name='companylot',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.company', verbose_name='Власник'),
        ),
        migrations.AlterField(
            model_name='companyreview',
            name='comment_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.client'),
        ),
    ]