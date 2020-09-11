from django import template

register = template.Library()


@register.filter
def attempted(question, user):
    return question.attempted(user)


@register.filter
def which(question, user):
    return question.which(user)


@register.filter
def what(question, user):
    return question.what(user)


@register.filter
def number(question, user):
    return question.number(user)


@register.filter
def lookup(lis, key):
    return lis[key]
