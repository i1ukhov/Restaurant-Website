import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))
