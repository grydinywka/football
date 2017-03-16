from django import template
from django.db.models import Q

register = template.Library()

@register.filter
def title_filter(queryset, player):
    print queryset
    print '__' + player + '__'
    if player:
        return queryset.filter(
             Q(contestant1__first_name__icontains=player) |
             Q(contestant2__first_name__icontains=player) |
             Q(contestant1__last_name__icontains=player) |
             Q(contestant2__last_name__icontains=player)
             )
    return queryset

register.filter('title_filter', title_filter)