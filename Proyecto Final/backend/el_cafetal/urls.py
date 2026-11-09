"""
El router de DRF genera automáticamente las URL de cada ViewSet:
/categorias/, /categorias/{id}/, /productos/ y /productos/{id}/
"""
from rest_framework.routers import DefaultRouter

from .views import categoria_views, producto_views, detalle_venta_views, venta_views

router = DefaultRouter()
router.register("categoria", categoria_views)
router.register("producto", producto_views)
router.register("detalle_venta", detalle_venta_views)
router.register("venta", venta_views)


urlpatterns = router.urls
