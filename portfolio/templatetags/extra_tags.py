from typing import Type, Optional, Dict, Any

from django import template
from django.forms import Form
from django.urls import reverse_lazy

register = template.Library()

@register.inclusion_tag('portfolio/components/action-btn.html')
def action_btn(btn_txt: str, id_prefix: str, style: str,
            section: Optional[bool] = True,
            url: Optional[str] = None,
            pk: Optional[int] = None,
            form: Optional[str] = None) -> Dict[str, Any]:
    args = [pk, ] if pk else None
    href = reverse_lazy(url, args=args) if url else '#'
    section = 'section' if section else ''
    return {
        'btn_txt': btn_txt,
        'id_prefix': id_prefix,
        'style': style,
        'section': section,
        'href': href,
        'pk': pk,
        'form': form,
    }
