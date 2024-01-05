from django import template
import math

register = template.Library()

@register.filter(name='ceil')
def ceil(value):
    print(value)
    return math.ceil(float(value))


@register.filter(name='neg')
def neg(value):
    print(value)
    return int(-value)

@register.filter(name='sub')
def sub(value, arg):
    return int(value) - int(arg)