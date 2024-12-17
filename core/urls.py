from django.urls import path
from core.views import categoria_produtos, index, lista_produtos, lista_categorias, lista_vendedores, descricao_vendedores, detalhes_produto


app_name = "core"

urlpatterns = [
    path("", index, name="index"), #Página Inicial
    path("produtos/", lista_produtos, name="product-list"), #Página de produtos divulgados
    path("produto/<pid>/", detalhes_produto, name="product-detail"), #Página de detalhes sobre um produto selecionado
    path("categoria/", lista_categorias, name="category-list"), #Página de categorias
    path("categoria/<cid>", categoria_produtos, name="category-product-list"), #Página de seleção de determinada categoria específica, onde listam os produtos daquela categoria
    path("vendedores/", lista_vendedores, name="vendor-list"), #Página de lista de vendedores da plataforma
    path("vendedor/<vid>", descricao_vendedores, name="vendor-detail"), #Página de um vendedor específico selecionado
]
