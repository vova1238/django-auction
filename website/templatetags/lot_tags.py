from django import template
from website.models import CompanyLot

register = template.Library()

@register.inclusion_tag('tags/last_lots.html')
def get_last_lots(count=5):
    lots = CompanyLot.objects.filter(is_active=True).order_by("-id")[:count]
    return {'last_lots': lots}
