from django import template
register = template.Library()


@register.filter
def index(d, key,name="index"):
    return d[key]
