from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/compra/', views.compra, name='compra'),
    path('producto/nuevo/', views.ProductoCreateView.as_view(), name='producto_crear'),
    path('producto/editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    path('producto/eliminar/<int:pk>/', views.ProductoDeleteView.as_view(), name='producto_eliminar'),
    path('reporte/agrupado/', views.reporte_agrupado, name='reporte_agrupado'),
    path('reporte/stock/', views.reporte_stock_critico, name='reporte_stock'),
    path('contacto/', views.contacto_cliente, name='contacto'),
]