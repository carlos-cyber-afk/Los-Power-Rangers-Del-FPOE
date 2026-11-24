"""
El router de DRF genera automáticamente las URL de cada ViewSet:
/api/productos/, /api/ventas/ y /api/detalles/ (y sus versiones con /{id}/)
"""
from rest_framework.routers import DefaultRouter

from .views import (producto_views, detalle_venta_views, venta_views)

router = DefaultRouter()
router.register("productos", producto_views)
router.register("detalles", detalle_venta_views)
router.register("ventas", venta_views)


urlpatterns = router.urls