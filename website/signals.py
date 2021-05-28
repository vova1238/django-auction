from django.db.models.signals import post_save

from celery_app.tasks import company_lot_end_task
from website.models import CompanyLot


def company_lot_saved(sender, instance, created, **kwargs):
    if instance.is_active:
        company_lot_end_task.apply_async(args=(instance.id,), eta=instance.date_end,)

post_save.connect(company_lot_saved, sender=CompanyLot)
