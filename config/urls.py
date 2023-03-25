from api.views import TestViewSet
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path
router = DefaultRouter()
router.register("test", TestViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += router.urls
