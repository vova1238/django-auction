# Generated by Django 3.1.7 on 2021-04-06 14:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(verbose_name='Опис')),
                ('url', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=100, size=[150, 150], upload_to='profiles/%Y/%m/%d', verbose_name='Зображення профілю')),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Номер телефону повинен бути введений у форматі: '+380XXXXXXXXX", regex='((\\+38)?\\(?\\d{3}\\)?[\\s\\.-]?(\\d{7}|\\d{3}[\\s\\.-]\\d{2}[\\s\\.-]\\d{2}|\\d{3}-\\d{4}))')], verbose_name='Телефон')),
                ('name', models.CharField(max_length=100, verbose_name='ПІБ')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClientLot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Назва лоту')),
                ('description', models.TextField(verbose_name='Опис')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('price_gap', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_end', models.DateTimeField(auto_now_add=True)),
                ('url', models.SlugField(unique=True)),
                ('lot_type', models.CharField(default='reverse_auction', editable=False, max_length=50)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.category', verbose_name='Category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.client', verbose_name='Лот')),
            ],
            options={
                'verbose_name': 'Лот',
                'verbose_name_plural': 'Лоти',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=100, size=[150, 150], upload_to='profiles/%Y/%m/%d', verbose_name='Зображення профілю')),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Номер телефону повинен бути введений у форматі: '+380XXXXXXXXX", regex='((\\+38)?\\(?\\d{3}\\)?[\\s\\.-]?(\\d{7}|\\d{3}[\\s\\.-]\\d{2}[\\s\\.-]\\d{2}|\\d{3}-\\d{4}))')], verbose_name='Телефон')),
                ('name', models.CharField(max_length=100, verbose_name='Назва компанії')),
                ('edrpou', models.PositiveIntegerField(blank=True, null=True, verbose_name='ЄДРПОУ')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='Місцезнаходження')),
                ('website_link', models.URLField(blank=True, verbose_name='Вебсайт')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompanyLot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Назва лоту')),
                ('description', models.TextField(verbose_name='Опис')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('price_gap', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_end', models.DateTimeField(auto_now_add=True)),
                ('url', models.SlugField(unique=True)),
                ('lot_type', models.CharField(default='auction', editable=False, max_length=50)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.category', verbose_name='Category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.company', verbose_name='Лот')),
            ],
            options={
                'verbose_name': 'Лот',
                'verbose_name_plural': 'Лоти',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LotPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='PNG', keep_meta=True, null=True, quality=100, size=[1000, 1000], upload_to='lot_photos/%Y/%m/%d', verbose_name='Картинка')),
                ('lot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.companylot')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Опис')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('rating', models.PositiveSmallIntegerField(verbose_name='Оцінка')),
                ('comment_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.clientlot')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.companylot')),
            ],
        ),
        migrations.CreateModel(
            name='ClientReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Опис')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('rating', models.PositiveSmallIntegerField(verbose_name='Оцінка')),
                ('comment_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.companylot')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.clientlot')),
            ],
        ),
    ]
