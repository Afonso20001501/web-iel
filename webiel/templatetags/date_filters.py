from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def add_days(value, days):
    if isinstance(value, datetime):
        value = value.date()
    return value + timedelta(days=int(days))