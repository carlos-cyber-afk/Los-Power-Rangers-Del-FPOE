from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UvaViewSet 

router = DefaultRouter()
router.register(r'uvas', UvaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]