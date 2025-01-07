from userauths.models import User
from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max

def default(request):
    categorias = Categoria.objects.all()
    vendedores = Vendedor.objects.all()
    min_max_preco = Produto.objects.aggregate(Min("preco"), Max("preco"))

    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.filter(user=request.user)
        except Wishlist.DoesNotExist:
            wishlist = 0
    else:
        wishlist = 0

    context = {
        'min_max_preco': min_max_preco,
        'categorias': categorias,
        'vendedores': vendedores,
        'wishlist': wishlist,
    }
    if request.user.is_authenticated:
        try:
            endereco = Endereco.objects.filter(user=request.user.id).first()
            context['endereco'] = endereco
        except Endereco.DoesNotExist:
            context['endereco'] = None
    return context
