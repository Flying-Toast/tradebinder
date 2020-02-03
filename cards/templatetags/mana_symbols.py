from django import template
from django.templatetags.static import static
from django.utils.encoding import escape_uri_path
from django.utils.safestring import mark_safe


register = template.Library()

def _render_code(code):
    if code == "½":
        code = "HALF"
    elif code == "∞":
        code = "INFINITY"
    elif "/" in code:
        code = "".join(code.split("/"))
    url = static(f"cards/symbols/{code}.svg")
    return f'<img class="mana-symbol" src="{escape_uri_path(url)}"></img>'


@register.filter()
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
            rendered_text += _render_code(code)
            code = ""
            continue
        if inside:
            code += ch
        else:
            rendered_text += ch
    return mark_safe(rendered_text)
