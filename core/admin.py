from django.contrib import admin
from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco

class ImagemProdutoAdmin(admin.TabularInline):
    model = ImagemProduto

class ProdutoAdmin(admin.ModelAdmin):
    inlines = [ImagemProdutoAdmin]
    list_display = ['user', 'titulo', 'imagem_produto', 'preco', 'categoria', 'vendedor', 'destaque', 'status_produto', 'pid']


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'imagem_categoria' ]


class VendedorAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'imagem_vendedor' ]


class PedidoCarrinhoAdmin(admin.ModelAdmin):
    list_editable = ['status_pagamento', 'status_produto']
    list_display = ['user', 'preco', 'status_pagamento','data_pedido', 'status_produto']


class ItensPedidoCarrinhoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'num_fatura', 'item','imagem', 'qtd', 'preco', 'total']


class AvaliacaoProdutoAdmin(admin.ModelAdmin):
    list_display = ['user', 'produto', 'avaliacao', 'classificacao' ]


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'produto', 'data' ]


class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['user', 'endereco', 'status' ]



admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Vendedor, VendedorAdmin)
admin.site.register(PedidoCarrinho, PedidoCarrinhoAdmin)
admin.site.register(ItensPedidoCarrinho, ItensPedidoCarrinhoAdmin)
admin.site.register(AvaliacaoProduto, AvaliacaoProdutoAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Endereco, EnderecoAdmin)
