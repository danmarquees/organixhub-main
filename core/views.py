from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.db.models import Count
from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco


def index(request):
    produto = Produto.objects.filter(status_produto="published", destaque=True)
    vendedores = Vendedor.objects.all()

    context = {
        "produtos": produto,
        "vendedores": vendedores,
        "categorias": Categoria.objects.all()
    }
    return render(request, 'core/index.html', context)


def lista_produtos(request):
    produtos = Produto.objects.filter(status_produto="published")
    context = {"produtos": produtos}
    return render(request, 'core/product-list.html', context)


def lista_categorias(request):
    categorias = Categoria.objects.all().annotate(produto_count=Count('categoria', 'produtos'))
    context = {"categorias": categorias}
    return render(request, 'core/category-list.html', context)


def categoria_produtos(request, cid):
    categoria = Categoria.objects.get(cid=cid)
    produtos = Produto.objects.filter(status_produto="published", categoria=categoria)
    context = {"categoria": categoria, "produtos": produtos}
    return render(request, "core/category-product-list.html", context)


def lista_vendedores(request): # Alteração aqui
    vendedores = Vendedor.objects.all()
    context = {"vendedores": vendedores, "categorias": Categoria.objects.all()} #Passando categorias também
    return render(request, "core/vendor-list.html", context)


def descricao_vendedores(request, vid):
    vendedor = get_object_or_404(Vendedor, vid=vid) # Utiliza get_object_or_404 para um tratamento de erro 404 mais limpo
    produtos = Produto.objects.filter(vendedor=vendedor, status_produto="published")
    context = {
        "vendedor": vendedor,
        "produtos": produtos,
    }
    return render(request, "core/vendor-detail.html", context)
