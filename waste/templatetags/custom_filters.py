from django import template
import datetime

register = template.Library()

@register.filter
def format_duration(value):
    if not isinstance(value, datetime.timedelta):
        return value
    total_seconds = int(value.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}min {seconds}s"
