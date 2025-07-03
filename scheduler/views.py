from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse(b"Hello, World! Welcome to Schedura, a scheduling app made with Django!")