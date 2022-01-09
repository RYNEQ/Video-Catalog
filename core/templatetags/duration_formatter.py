from django import template

register = template.Library()

@register.filter
def duration_formatter(v):
    hours = v // 3600
    mins = (v % 3600) // 60
    secs = v - (hours * 3600 + mins * 60)
    return f'{hours}:{mins}:{secs}'



# register.filter('du', duration_formatter)
