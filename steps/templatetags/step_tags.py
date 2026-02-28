from django import template

register = template.Library()


@register.filter
def get_item(dictionary: dict, key: object) -> object:
    """Get an item from a dictionary by key in templates."""
    return dictionary.get(key)
