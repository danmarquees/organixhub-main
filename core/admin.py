from django.contrib import admin
from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco

class ImagemProdutoAdmin(admin.TabularInline):
    model = ImagemProduto

class ProdutoAdmin(admin.ModelAdmin):
    inlines = [ImagemProdutoAdmin]
    list_display = ['usuario', 'titulo', 'imagem_produto', 'preco', 'destaque', 'status_produto']


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'imagem_categoria' ]


class VendedorAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'imagem_vendedor' ]


class PedidoCarrinhoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'preco', 'status_pagamento','data_pedido', 'status_produto']


class ItensPedidoCarrinhoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'num_fatura', 'item','qtd', 'preco', 'total']


class AvaliacaoProdutoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'produto', 'avaliacao', 'classificacao' ]


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'produto', 'data' ]


class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'endereco', 'status' ]



admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Vendedor, VendedorAdmin)
admin.site.register(PedidoCarrinho, PedidoCarrinhoAdmin)
admin.site.register(ItensPedidoCarrinho, ItensPedidoCarrinhoAdmin)
admin.site.register(AvaliacaoProduto, AvaliacaoProdutoAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Endereco, EnderecoAdmin)
