from django.contrib import admin
from .models import Event, Resource, ResourceCategory, EventType

admin.site.register(Event)
admin.site.register(Resource)
admin.site.register(ResourceCategory)
admin.site.register(EventType)
