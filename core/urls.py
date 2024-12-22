from django.urls import path
from django import views
from core.views import categoria_produtos, index, lista_produtos, lista_categorias, lista_vendedores, descricao_vendedores, detalhes_produto, tag_list, ajax_add_review,search, filter_product


app_name = "core"

urlpatterns = [
    path("", index, name="index"), #Página Inicial
    path("produtos/", lista_produtos, name="product-list"), #Página de produtos divulgados
    path("produto/<pid>/", detalhes_produto, name="product-detail"), #Página de detalhes sobre um produto selecionado
    path("categoria/", lista_categorias, name="category-list"), #Página de categorias
    path("categoria/<cid>", categoria_produtos, name="category-product-list"), #Página de seleção de determinada categoria específica, onde listam os produtos daquela categoria
    path("vendedores/", lista_vendedores, name="vendor-list"), #Página de lista de vendedores da plataforma
    path("vendedor/<vid>", descricao_vendedores, name="vendor-detail"), #Página de um vendedor específico selecionado
    path("produtos/tag/<slug:tag_slug>/", tag_list, name="tags"), #Pagina de Tags selecionadas
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review"), #Reviews e Estrelas
    path("search/", search, name="search"),
    path("filter-products", filter_product, name='filter-product'),
]
