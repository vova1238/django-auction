from django.contrib.auth.models import User
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from website.utils import slugify


# Abstract user
class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = ResizedImageField("Зображення профілю", size=[150, 150], upload_to="profiles/%Y/%m/%d", null=True, blank=True)

    phone_regex = RegexValidator(regex=r'((\+38)?\(?\d{3}\)?[\s\.-]?(\d{7}|\d{3}[\s\.-]\d{2}[\s\.-]\d{2}|\d{3}-\d{4}))', message="Номер телефону повинен бути введений у форматі: '+380XXXXXXXXX")
    phone = models.CharField("Телефон", validators=[phone_regex], max_length=17, blank=True)

    class Meta:
        abstract = True


# Created users
class Client(SiteUser):
    name = models.CharField("ПІБ", max_length=100)
    # lot = models.ForeignKey(ClientLot, verbose_name="Лот", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"
    

class Company(SiteUser):
    name = models.CharField("Назва компанії", max_length=100)
    edrpou = models.PositiveIntegerField("ЄДРПОУ", blank=True, null=True)
    location = models.CharField("Місцезнаходження", max_length=100, blank=True)
    website_link = models.URLField("Вебсайт", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Компанія"
        verbose_name_plural = "Компанії"


# Lot category
class Category(models.Model):
    name = models.CharField("Назва категорії", max_length=150)
    description = models.TextField("Опис")
    url = models.SlugField("Посилання", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def get_absolute_url(self):
        return f"{reverse('lots')}?category={self.url}"


# Lot
class Lot(models.Model):
    name = models.CharField("Назва лоту", max_length=255)
    description = models.TextField("Опис")
    
    category = models.ForeignKey(
        Category, verbose_name="Категорія", on_delete=models.SET_NULL, null=True
    )
    
    price = models.PositiveIntegerField("Стартова ціна")
    current_price = models.PositiveIntegerField("Ціна зараз", default = None, blank=True, null=True)
    price_gap = models.PositiveIntegerField("Зміна ціни", help_text = "(Ціна, на яку можуть змінювати ціну ставки)", blank=True, default=30)
    date_created = models.DateTimeField("Створено", auto_now_add=True, editable=False)
    date_end = models.DateTimeField("Завершується")
    url = models.SlugField("Посилання", unique=True, blank=True, null=True)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse("lot_detail", kwargs={"slug": self.url})
    
    


class ClientLot(Lot):
    owner = models.ForeignKey(Client, verbose_name="Власник лоту", on_delete=models.CASCADE)
    lot_type = models.CharField(max_length=50, editable=False, default="reverse_auction")

    def __str__(self):
        return str(self.owner)

    class Meta:
        verbose_name = "Лот клієнта"
        verbose_name_plural = "Лоти клієнта"

    def save(self, *args, **kwargs):
        # Do if this is a new instance
        if not self.pk:
            self.current_price = self.price

            slug = slugify(self.name)[:50]
            if not ClientLot.objects.filter(url = slug).exists():
                self.url = slug
            else:
                super(ClientLot, self).save(*args, **kwargs)
                id_length = len(str(self.id)) + 1
                slugify(self.name)[:50 - id_length]
                self.url = slug  + '-' + str(self.id)
            
        super(ClientLot, self).save(*args, **kwargs)

class CompanyLot(Lot):
    owner = models.ForeignKey(Company, verbose_name="Власник лоту", on_delete=models.CASCADE)
    lot_type = models.CharField(max_length=50, editable=False, default="auction")

    def __str__(self):
        return f'{self.name} - ({self.owner})'

    class Meta:
        verbose_name = "Лот компанії"
        verbose_name_plural = "Лоти компаній"

    def first_image(self):
        return self.images.first()

    def save(self, *args, **kwargs):
        # Do if this is a new instance
        if not self.pk:
            self.current_price = self.price
        
            slug = slugify(self.name)[:50]
            # Create slug if it does not exists yet
            if not CompanyLot.objects.filter(url = slug).exists():
                self.url = slug
            # If slug exists add lot id to the end of the slug
            else:
                super(CompanyLot, self).save(*args, **kwargs)
                id_length = len(str(self.id)) + 1
                slugify(self.name)[:50 - id_length]
                self.url = slug  + '-' + str(self.id)
        
        super(CompanyLot, self).save(*args, **kwargs)

class LotPhoto(models.Model):
    photo = ResizedImageField('Фото', crop=['middle', 'center'], upload_to="lot_photos/%Y/%m/%d", null=True)
    lot = models.ForeignKey(
        CompanyLot, on_delete=models.CASCADE,
        related_name='images'
    )

    class Meta:
        verbose_name = "Фотографія лота"
        verbose_name_plural = "Фотографії лотів"

    def __str__(self):
        return f'{self.lot.name} - ({self.lot.owner})'


class BidClientLot(models.Model):
    lot = models.ForeignKey(
        ClientLot, on_delete = models.CASCADE
    )
    hiden_name = models.CharField("Ім'я", max_length=255)
    price = models.PositiveIntegerField("Ставка")
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Ставка на лот клієнта"
        verbose_name_plural = "Ставки на лот клієнта"

class BidCompanyLot(models.Model):
    lot = models.ForeignKey(
        CompanyLot, on_delete = models.CASCADE
    )
    bidder = models.ForeignKey(Client, verbose_name='bid', on_delete = models.CASCADE, default=None)
    hiden_name = models.CharField("Ім'я", max_length=255)
    price = models.PositiveIntegerField("Ставка")
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Ставка на лот компанії"
        verbose_name_plural = "Ставки на лот компанії"

    def __str__(self):
        return self.hiden_name


# Reviews
class CompanyReview(models.Model):
    lot = models.ForeignKey(CompanyLot, on_delete=models.CASCADE)
    comment_owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    description = models.TextField("Опис")
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    rating = models.SmallIntegerField(default=0, 
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
    ]
    )

    def __str__(self):
        return str(self.comment_owner)

    class Meta:
        verbose_name = "Відгук клієнта"
        verbose_name_plural = "Відгуки клієнтів"
    


class ClientReview(models.Model):
    lot = models.ForeignKey(ClientLot, on_delete=models.CASCADE)
    comment_owner = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField("Опис")
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    rating = models.SmallIntegerField(default=0, 
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
    ]
    )

    def __str__(self):
        return str(self.comment_owner)

    class Meta:
        verbose_name = "Відгук компанії"
        verbose_name_plural = "Відгуки компаній"
