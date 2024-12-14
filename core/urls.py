from django.urls import path
from core.views import index, lista_produtos, lista_categorias


app_name = "core"

urlpatterns = [
   path("", index, name="index"),
    path("produtos/", lista_produtos, name="product-list"),
   path("categoria/", lista_categorias, name="category-list")
]
