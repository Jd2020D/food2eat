from django import template


register = template.Library()

@register.filter
def getValue(value,arg):
    if arg in value:
        return value[arg]-1
    return False


@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def sub1(value):
    return value -1

@register.filter
def getDate(value,arg):
    print(value)
    print(value[arg])
    return value[arg]

@register.filter
def total(value):
    total=0
    for item in value.items.all():
        total+=item.quantity*item.meal.price
    return total

@register.filter
def getImage(value):
    if value.startswith('http'):
        return value
    else:
        return '/static/img/'+value

