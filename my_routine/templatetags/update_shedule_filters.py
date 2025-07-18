from django import template
from ..models import Details

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_shift(details, shift):
    try:
        return details.get(shift=shift)
    except Details.DoesNotExist:
        return None
