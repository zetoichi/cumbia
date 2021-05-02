from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<html><title>Cumbia</title></html>')