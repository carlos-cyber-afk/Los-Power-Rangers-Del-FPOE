from django.contrib import admin

from .models import producto, venta, detalle_venta

admin.site.register(producto)
admin.site.register(venta)
admin.site.register(detalle_venta)