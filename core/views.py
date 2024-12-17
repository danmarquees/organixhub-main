from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.db.models import Count
from taggit.models import Tag
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
    vendedores = Vendedor.objects.all()

    context = {
        "produtos": produtos,
        "vendedores": vendedores,
        "categorias": Categoria.objects.all()

    }
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
    categorias = Categoria.objects.all()
    vendedores = Vendedor.objects.all() #Adi
    context = {
        "vendedor": vendedor,
        "produtos": produtos,
        "categorias": categorias,
        "vendedores": vendedores,
    }
    return render(request, "core/vendor-detail.html", context)


def detalhes_produto(request, pid):
    produto = Produto.objects.get(pid=pid)
    produto = get_object_or_404(Produto, pid=pid)
    produtos = Produto.objects.filter(categoria=produto.categoria).exclude(pid=pid)
    categorias = Categoria.objects.all()
    vendedores = Vendedor.objects.all() #Adicione esta linha

    p_imagem = produto.p_imagem.all()

    context = {
        "p": produto,
        "p_imagem": p_imagem,
        "categorias": categorias,
        "vendedores": vendedores, #Adicione aqui
        "produtos": produtos,

    }

    return render (request, "core/product-detail.html", context)


def tag_list(request, tag_slug=None):
    produtos = Produto.objects.filter(status_produto="published").order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        produtos = produtos.filter(tags__in=[tag])

    context = {
        "produtos": produtos,
        "tag": tag
    }

    return render(request, "core/tag.html", context)
