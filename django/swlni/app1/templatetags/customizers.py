from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def highlight_search1(text, search_term):
    highlighted = text.replace(search_term, f'<span class="highlight">{search_term}</span>')
    return mark_safe(highlighted)

@register.filter()
def highlight_search(text, search_term):
    if text is not None:
        text = str(text)
        src_str = re.compile(search_term, re.IGNORECASE)
        str_replaced = src_str.sub(f'<span class="highlight">{search_term}</span>', text)
    else:
        str_replaced = ''
    return mark_safe(str_replaced)