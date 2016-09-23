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
    if int(value) < 30:
        t = int(value) + 2000
    else:
        t = int(value) + 1900
    v = str(t)[2:]
    return v



