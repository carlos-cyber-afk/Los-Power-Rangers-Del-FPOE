from django.contrib import admin

from .models import categoria, detalle_venta, producto, venta

admin.site.register(categoria)
admin.site.register(producto)
admin.site.register(venta)
admin.site.register(detalle_venta)
