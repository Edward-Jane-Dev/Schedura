from django.db import models

# Create your models here.

class ResourceCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class EventType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    block_resource = models.BooleanField(default=False) # type: ignore

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    is_recurring = models.BooleanField(default=False) # type: ignore
    recurrence_rule = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
