# templatetags/shedule_filters.py
from django import template
from ..models import Shedule, Shift, Details

register = template.Library()

@register.filter
def get_day(shedules, day):
    try:
        return shedules.get(day=day)
    except Shedule.DoesNotExist:
        return None

@register.filter
def get_shift(details, shift):
    try:
        return details.get(shift=shift)
    except Details.DoesNotExist:
        return None
