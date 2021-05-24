import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from project.celery import app
from website.models import CompanyLot


def mail_winner(company_lot):
    last_bid = company_lot.bidcompanylot_set.last()
    if last_bid:
        msg_html = render_to_string('celery_app/winner_email.html', {'lot':company_lot,'winner': last_bid.bidder, 'domain': 'http://127.0.0.1:8000'})
        try:
            send_mail(
                f'Ви перемогли в торгах за лот {company_lot.name}',
                "",
                'chernivtsi.auction@gmail.com',
                [last_bid.bidder.user.email],
                fail_silently=False,
                html_message=msg_html
            )
        except last_bid.bidder.DoesNotExist:
            logging.warning(f"Tried to send email to non-existing user {last_bid.bidder.name}")

        return f"У лоті {company_lot} переміг {last_bid.bidder.name}"
    else:
        return f"Ніхто не брав участі в торгах за лот {company_lot}"

@app.task
def company_lot_end_task(company_lot_id):
    try:
        company_lot = CompanyLot.objects.get(id=company_lot_id)
        company_lot.is_active = False
        company_lot.save()
        mail_winner(company_lot)
    except CompanyLot.DoesNotExist as e:
        print("Лот не знайдено", e)
