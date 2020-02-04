from django import template
from django.templatetags.static import static
from django.utils.encoding import escape_uri_path
from django.utils.safestring import mark_safe
from django.utils.html import escape
from cards import models


register = template.Library()

def render_code(code):
    if code == "½":
        code = "HALF"
    elif code == "∞":
        code = "INFINITY"
    alt_code = code
    if "/" in code:
        code = code.replace("/", "")
    url = static(escape_uri_path(f"cards/symbols/{code}.svg"))
    return f'<img class="mana-symbol" src="{url}" alt="{escape(f"{{{alt_code}}}")}">'


@register.filter
def render_symbols(text):
    if len(text) == 0:
        return ""

    rendered_text = ""
    idx = 0
    ch = ""
    inside = False
    code = ""
    while idx <= len(text) - 1:
        ch = text[idx]
        idx += 1

        if ch == "{":
            inside = True
            continue
        if ch == "}":
            inside = False
            rendered_text += render_code(code)
            code = ""
            continue
        if inside:
            code += ch
        else:
            rendered_text += ch
    return mark_safe(rendered_text)


@register.simple_tag
def card_img(card):
    if not isinstance(card, models.Card):
        raise TypeError("The card_img tag requires a 'cards.models.Card' as the argument")
    return static(escape_uri_path(f"cards/card_imgs/{card.id}.jpg"))
