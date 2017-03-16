from django import template

register = template.Library()


@register.filter
def cont_exclude(queryset, contestant):
    return queryset.exclude(pk=contestant.pk)




register.filter('cont_exclude', cont_exclude)
