from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco


def default(request):
    categoria = Categoria.objects.all()

    return {
        'categorias': categoria,
    }
