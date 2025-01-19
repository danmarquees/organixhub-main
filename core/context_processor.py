# Importa o modelo de usuário, mas não é usado.  Considere removê-lo se não for necessário.
from userauths.models import User
# Importa modelos do aplicativo core. Alguns modelos importados não são usados.
from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco
# Importa o decorador login_required, mas não é usado.  Considere removê-lo se não for necessário.
from django.contrib.auth.decorators import login_required
# Importa as funções Min e Max para agregar valores mínimos e máximos.
from django.db.models import Min, Max

# Define uma função que retorna um contexto para um template.
def default(request):
    # Recupera todas as categorias.
    categorias = Categoria.objects.all()
    # Recupera todos os vendedores.
    vendedores = Vendedor.objects.all()
    # Calcula o preço mínimo e máximo dos produtos.
    min_max_preco = Produto.objects.aggregate(Min("preco"), Max("preco"))

    # Verifica se o usuário está autenticado.
    if request.user.is_authenticated:
        try:
            # Se sim, recupera a lista de desejos do usuário.
            wishlist = Wishlist.objects.filter(user=request.user)
        # Trata o caso em que o usuário não tem uma lista de desejos.
        except Wishlist.DoesNotExist:
            wishlist = 0
    # Se o usuário não está autenticado, define a lista de desejos como 0.
    else:
        wishlist = 0

    # Cria um dicionário de contexto para o template.
    context = {
        'min_max_preco': min_max_preco,
        'categorias': categorias,
        'vendedores': vendedores,
        'wishlist': wishlist,
    }
    # Verifica se o usuário está autenticado.
    if request.user.is_authenticated:
        try:
            # Se sim, recupera o endereço do usuário.
            endereco = Endereco.objects.filter(user=request.user.id).first()
            # Adiciona o endereço ao contexto do template.
            context['endereco'] = endereco
        # Trata o caso em que o usuário não tem um endereço cadastrado.
        except Endereco.DoesNotExist:
            context['endereco'] = None
    # Retorna o contexto para o template.
    return context
