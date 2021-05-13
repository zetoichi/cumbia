import json
from django.views.generic.base import TemplateView

from .models import Photographer
# fake_api = '/Users/Zeta/code/projects/work/cumbia/portfolio/fake_api.json'

# with open(fake_api, 'r') as f:
#     photographers = json.load(f)

class IndexView(TemplateView):
    template_name = 'portfolio/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photographers'] = Photographer.objects.all()
        return context
