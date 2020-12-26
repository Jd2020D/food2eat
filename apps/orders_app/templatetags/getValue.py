from django import template
register = template.Library()

@register.filter
def getValue(value,arg):
    print (value)
    print('oooooooooooo')
    print(arg)
    if arg in value:
        return value[arg]-1
    return False


@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def sub1(value):
    return value -1
