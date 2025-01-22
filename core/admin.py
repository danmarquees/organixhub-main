from django.contrib import admin
from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Coupon, Endereco

class ImagemProdutoAdmin(admin.TabularInline):
    model = ImagemProduto

class ProdutoAdmin(admin.ModelAdmin):
    inlines = [ImagemProdutoAdmin]
    list_display = ['user', 'titulo', 'imagem_produto', 'preco', 'categoria', 'vendedor', 'destaque', 'status_produto', 'pid', 'get_badges']
    def get_badges(self, obj):
        return ", ".join(obj.badges) if obj.badges else "Sem Badges"
    get_badges.short_description = "Badges"


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'imagem_categoria' ]


class VendedorAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'imagem_vendedor' ]


class PedidoCarrinhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status_pagamento', 'paypal_txn_id', 'payment_date', 'preco')
    search_fields = ('id', 'paypal_txn_id', 'user__username')
    list_filter = ('status_pagamento', 'payment_date')




class ItensPedidoCarrinhoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'num_fatura', 'item','imagem', 'qtd', 'preco', 'total']


class AvaliacaoProdutoAdmin(admin.ModelAdmin):
    list_display = ['user', 'produto', 'avaliacao', 'classificacao' ]


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'produto', 'data' ]


class EnderecoAdmin(admin.ModelAdmin):
    list_editable = ['cep', 'logradouro', 'complemento', 'bairro', 'localidade', 'uf', 'numero', 'status', 'celular']
    list_display = ['user', 'cep', 'logradouro', 'complemento', 'bairro', 'localidade', 'uf', 'numero', 'status', 'celular' ]

class CouponAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'desconto', 'ativo', 'data_criacao', 'data_validade', 'valor_minimo', 'usos_maximos', 'usos_atuais']
    list_editable = ['ativo', 'data_validade', 'valor_minimo', 'usos_maximos']
    search_fields = ['codigo']
    list_filter = ['ativo', 'data_criacao', 'data_validade']


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Vendedor, VendedorAdmin)
admin.site.register(PedidoCarrinho, PedidoCarrinhoAdmin)
admin.site.register(ItensPedidoCarrinho, ItensPedidoCarrinhoAdmin)
admin.site.register(AvaliacaoProduto, AvaliacaoProdutoAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Coupon, CouponAdmin)
