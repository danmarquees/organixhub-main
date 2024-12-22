from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco
from django.contrib.auth.decorators import login_required



def default(request):
    categoria = Categoria.objects.all()
    endereco = Endereco.objects.get(user=request.user)
    vendedores = Vendedor.objects.all()

    return {
        'categorias': categoria,
        'endereco': endereco,
        'vendedores': vendedores

    }


def default(request):
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
