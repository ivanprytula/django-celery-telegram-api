from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='str_to_lowercase')
@stringfilter
def sting_value_to_lowercase(value):
    return value.lower()
