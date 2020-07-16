from django import template

register = template.Library()


@register.filter
def liked(comment, user):
    return comment.is_liked(user)


@register.filter
def viewed(obj, user):
    return obj.is_viewed(user)
