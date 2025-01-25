from django.urls import path
from useradmin import views

app_name = "useradmin"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("produtos/", views.products, name="products"),
    path("adicionar-produto/", views.add_product, name="add-product"),
]
