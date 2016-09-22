from django import template

register = template.Library()

@register.filter
def ListIndex(value, arg):
    try:
        return list(value[int(arg)])
    except:
        return ''

@register.filter
def GetHakbun(value):
    v = str(value)[2:]
    return v

