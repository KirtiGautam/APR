from django import template

register = template.Library()


@register.filter
def liked(comment, user):
    return comment.is_liked(user)
