from django.db.models.aggregates import Avg
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.db.models import Count, Avg
from taggit.models import Tag
from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco
from core.forms import AvaliacaoProdutoForm
from userauths.models import User
from django.utils import timezone


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
    produto = get_object_or_404(Produto, pid=pid)
    produtos = Produto.objects.filter(categoria=produto.categoria).exclude(pid=pid)
    categorias = Categoria.objects.all()
    vendedores = Vendedor.objects.all()
    reviews = AvaliacaoProduto.objects.filter(produto=produto).order_by("-data")

    # Corrected aggregation
    media_aval = AvaliacaoProduto.objects.filter(produto=produto).aggregate(average_classification=Avg('classificacao'))

    review_form = AvaliacaoProdutoForm()
    p_imagem = produto.p_imagem.all()

    context = {
        "p": produto,
        "review_form": review_form,
        "p_imagem": p_imagem,
        "media_aval": media_aval,
        "reviews": reviews,
        "categorias": categorias,
        "vendedores": vendedores,
        "produtos": produtos,
    }
    return render(request, "core/product-detail.html", context)


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


def ajax_add_review(request, pid):
    produto = get_object_or_404(Produto, pk=pid)
    user = request.user

    if request.method == 'POST':
        review_form = AvaliacaoProdutoForm(request.POST)
        if review_form.is_valid():
            try:
                review = review_form.save(commit=False)
                review.user = user
                review.produto = produto
                review.data = timezone.now()
                review.save()
                return JsonResponse({
                    'bool': True,
                    'context': {
                        'user': user.username,
                        'review': review.avaliacao,
                        'rating': review.classificacao,
                        'data': review.data.strftime("%d %b, %Y"),
                        'user_image': user.profile.image.url if hasattr(user, 'profile') and user.profile.image else None,
                    },
                    'media_aval': AvaliacaoProduto.objects.filter(produto=produto).aggregate(average_rating=Avg('classificacao'))
                })
            except ObjectDoesNotExist:
                return JsonResponse({'bool': False, 'errors': 'Usuário ou produto não encontrado'}, status=404)
            except IntegrityError:
                return JsonResponse({'bool': False, 'errors': 'Erro de integridade do banco de dados'}, status=500)
            except ValueError as e:
                return JsonResponse({'bool': False, 'errors': f'Erro de valor: {e}'}, status=500)
            except Exception as e:
                return JsonResponse({'bool': False, 'errors': f'Erro inesperado: {e}'}, status=500)
        else:
            return JsonResponse({'bool': False, 'errors': review_form.errors}, status=400)
    else:
        return JsonResponse({'bool': False, 'errors': 'Método de requisição inválido'}, status=405)


def search(request):
    query = request.GET.get("q")

    produtos = Produto.objects.filter(titulo__icontains=query).order_by("-data")

    context = {
        "produtos": produtos,
        "query": query,
    }
    return render(request, "core/search.html", context)
