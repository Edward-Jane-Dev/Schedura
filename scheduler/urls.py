from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'resources', views.ResourceViewSet)
router.register(r'resource-categories', views.ResourceCategoryViewSet)
router.register(r'event-types', views.EventTypeViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('api/', include(router.urls)),
]