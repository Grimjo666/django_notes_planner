from django import template

register = template.Library()


@register.filter(name='get')
def get(value, key):
    try:
        return value[key]
    except:
        return None
