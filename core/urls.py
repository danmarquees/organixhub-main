from django.urls import path, include
from django import views
from core.views import categoria_produtos, index, lista_produtos, lista_categorias, lista_vendedores, descricao_vendedores, detalhes_produto, tag_list, ajax_add_review,search, filter_product, about, privacy_policy, service_terms, add_to_cart, cart_view, delete_item_from_cart, update_from_cart, checkout, pagamento_efetuado,  pagamento_falha, customer_dashboard, order_detail, make_address_default, delete_address,  buscar_endereco, product_quickview,  add_to_wishlist, wishlist, delete_wishlist_item

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
    path("search/", search, name="search"), # Rota para a página de busca
    path("filter-products", filter_product, name='filter-product'), # Rota para filtragem de produtos via AJAX
    path("sobre-nos/", about, name='about' ), # Rota para a página "Sobre Nós"
    path("politica-de-privacidade/", privacy_policy, name='privacy-policy'), # Rota para a página de política de privacidade
    path("termos-de-servico/", service_terms, name='service-terms'), # Rota para a página de termos de serviço
    path("add-to-cart/", add_to_cart, name="add-to-cart"), # Rota para adicionar um produto ao carrinho
    path("carrinho/", cart_view, name="cart"), # Rota para visualizar o carrinho de compras
    path('delete-item-from-cart/', delete_item_from_cart, name='delete-item-from-cart'), # Rota para remover um item do carrinho
    path("update-cart/", update_from_cart, name='update-from-cart'), # Rota para atualizar a quantidade de um item no carrinho
    path("checkout/", checkout, name="checkout"), # Rota para a página de checkout
    path('paypal/', include('paypal.standard.ipn.urls')),
    path("pagamento-efetuado/", pagamento_efetuado, name="payment-completed"),
    path("pagamento-falha/", pagamento_falha, name="payment-failed"),
    path("dashboard/", customer_dashboard, name="dashboard"),
    path("dashboard/pedido/<int:id>", order_detail, name="order-detail"),
    path("make-address-default/", make_address_default, name="make-default-address"),
    path("delete-address/", delete_address, name="delete-address"),
    path('buscar-endereco/', buscar_endereco, name='buscar_endereco'),
    path('quickview/<int:pid>/', product_quickview, name='product_quickview'),
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),
    path("wishlist/", wishlist, name="wishlist"),
    path("delete-wishlist-item/", delete_wishlist_item, name="delete-wishlist-item"),
]
