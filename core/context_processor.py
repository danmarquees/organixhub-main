from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max


def default(request):
    categoria = Categoria.objects.all()
    endereco = Endereco.objects.get(user=request.user)
    vendedores = Vendedor.objects.all()

    min_max_preco = Produto.objects.aggregate(Min("preco"), Max("preco"))

    return{
        'min_max_preco': min_max_preco,
    }



    if request.user.is_authenticated:
        try:
            endereco = Endereco.objects.get(user=request.user)
            # ... seu código para usar endereco ...
            return {'endereco': endereco}
        except Endereco.DoesNotExist:
            # Lidar com o caso em que o usuário não tem um Endereco
            return {'endereco': None}  # Ou levantar uma exceção apropriada
    else:
        return {} # Retorna um dicionário vazio se o usuário não estiver autenticado



    return  {
        'categorias': categoria,
        'endereco': endereco,
        'vendedores': vendedores,
    }
