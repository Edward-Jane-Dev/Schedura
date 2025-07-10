from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import Event, Resource, ResourceCategory, EventType
from .serializers import EventSerializer, ResourceSerializer, ResourceCategorySerializer, EventTypeSerializer

# Create your views here.
def index(request):
    return HttpResponse(b"Hello, World! Welcome to Schedura, a scheduling app made with Django!")

def home(request):
    return render(request, 'home.html')

def schedule(request):
    return render(request, 'schedule.html')

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all() # type: ignore
    serializer_class = EventSerializer

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all() # type: ignore
    serializer_class = ResourceSerializer

class ResourceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ResourceCategory.objects.all() # type: ignore
    serializer_class = ResourceCategorySerializer

class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all() # type: ignore
    serializer_class = EventTypeSerializer