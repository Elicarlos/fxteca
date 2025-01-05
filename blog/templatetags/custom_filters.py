from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retorna o valor correspondente a uma chave em um dicionário."""
    return dictionary.get(key)
