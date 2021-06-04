from typing import Type, Optional, Dict, Any

from django import template
from django.forms import Form

register = template.Library()

# @register.inclusion_tag('tags/simple_form.html')
# def simple_tag() -> Dict[str, Any]:
#     """
#     """
#     context = {}
#     return context
