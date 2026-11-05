"""
El router de DRF genera automáticamente las URL de cada ViewSet:
/categorias/, /categorias/{id}/, /productos/ y /productos/{id}/
"""
from rest_framework.routers import DefaultRouter

from .views import UvaViewSet

router = DefaultRouter()
router.register("uvas", UvaViewSet)
urlpatterns = router.urls
