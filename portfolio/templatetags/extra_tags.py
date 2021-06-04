from typing import Type, Optional, Dict, Any

from django import template
from django.forms import Form

register = template.Library()

@register.inclusion_tag('tags/simple_form.html')
def simple_form(form: Type[Form], main_action: str = 'Enviar',
            secondary_action: Optional[str] = None) -> Dict[str, Any]:
    """
    """
    context = {
        'form': form,
        'main_action': main_action,
        'secondary_action': secondary_action,
    }
    return context
