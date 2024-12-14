from django.shortcuts import HttpResponse, render

from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco


def index(request):
    # produto = Produto.objects.all().order_by("-id")
    produto = Produto.objects.filter(status_produto="published", destaque=True)

    context = {
        "produtos": produto
    }

    return render(request, 'core/index.html', context)


def lista_produtos(request):
    produto = Produto.objects.filter(status_produto="published")

    context = {
        "produtos": produto
    }

    return render(request, 'core/product-list.html', context)


def lista_categorias(request):
    categoria = Categoria.objects.all()

    context = {
        "categorias": categoria
    }

    return render(request, 'core/product-list.html', context)
