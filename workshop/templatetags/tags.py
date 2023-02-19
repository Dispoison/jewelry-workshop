from django import template

register = template.Library()


@register.filter
def currency(number):
    return f"{number:,.2f}"


@register.inclusion_tag("workshop/index/category_item.html")
def show_category_item(category_item):
    return {"category_item": category_item}
