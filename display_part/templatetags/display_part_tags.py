from django import template
register = template.Library()


# @register.filter(name='addstr')
# def addstr(value, arg):
#     """ Only concat string argument """
#     return str(value) + str(arg)


@register.filter
def index(value, arg):
    return value[arg]
