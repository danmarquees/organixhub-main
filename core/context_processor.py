from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max


def default(request):
    categorias = Categoria.objects.all()
    vendedores = Vendedor.objects.all()
    min_max_preco = Produto.objects.aggregate(Min("preco"), Max("preco"))
    context = {
        'min_max_preco': min_max_preco,
        'categorias': categorias,
        'vendedores': vendedores,
    }
    if request.user.is_authenticated:
        try:
            endereco = Endereco.objects.get(user=request.user.id)
            context['endereco'] = endereco
        except Endereco.DoesNotExist:
            context['endereco'] = None
    return context
