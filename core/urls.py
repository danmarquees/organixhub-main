from django.urls import path
from core.views import categoria_produtos, index, lista_produtos, lista_categorias, lista_vendedores


app_name = "core"

urlpatterns = [

   #Página Inicial
   path("", index, name="index"),
   path("produtos/", lista_produtos, name="product-list"),

   #Categoria
   path("categoria/", lista_categorias, name="category-list"),
   path("categoria/<cid>", categoria_produtos, name="category-product-list"),

   #Vendedor
   path("vendedores/", lista_vendedores, name="vendor-list"),
]
