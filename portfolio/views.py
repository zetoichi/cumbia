import json
from django.shortcuts import render

fake_api = '/Users/Zeta/code/projects/work/cumbia/portfolio/fake_api.json'

with open(fake_api, 'r') as f:
    photographers = json.load(f)

def index(request):
    # context = {}
    # context['photographers'] = photographers
    return render(request, 'portfolio/index.html')