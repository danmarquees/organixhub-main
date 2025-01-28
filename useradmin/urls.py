from django.urls import path
from useradmin import views

app_name = "useradmin"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("produtos/", views.products, name="products"),
    path("adicionar-produto/", views.add_product, name="add-product"),
    path("editar-produto/<pid>/", views.edit_product, name="edit-product"),
    path("deletar-produto/<pid>/", views.delete_product, name="delete-product"),
    path("pedidos/", views.orders, name="orders"),
    path("detalhes-pedido/<id>/", views.order_detail, name="order-detail"),
]
