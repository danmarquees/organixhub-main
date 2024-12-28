from django.db.models.aggregates import Avg # Importa a função Avg para calcular a média
from django.http import JsonResponse # Importa JsonResponse para retornar respostas JSON
from django.shortcuts import HttpResponse, render, get_object_or_404, redirect # Importa funções para renderizar templates e lidar com requisições
from django.db.models import Count, Avg, Min, Max # Importa funções para contagem e agregação de dados
from taggit.models import Tag # Importa o modelo Tag para lidar com tags
from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, ImagemProduto, AvaliacaoProduto, Endereco # Importa modelos do aplicativo core
from core.forms import AvaliacaoProdutoForm # Importa o formulário para avaliações de produtos
from userauths.models import User # Importa o modelo de usuário
from django.utils import timezone # Importa funções relacionadas a data e hora
from django.template.loader import render_to_string


def index(request):
    # Busca produtos publicados e em destaque
    produto = Produto.objects.filter(status_produto="published", destaque=True)
    # Busca todos os vendedores
    vendedores = Vendedor.objects.all()

    # Calcula a média das avaliações para cada produto
    for p in produto:
        media_aval = AvaliacaoProduto.objects.filter(produto=p).aggregate(average_classification=Avg('classificacao'))
        if media_aval['average_classification'] is not None:
            p.media_avaliacoes = media_aval['average_classification']
        else:
            p.media_avaliacoes = 0



    # Cria o contexto para o template
    context = {
        "produtos": produto,
        "vendedores": vendedores,
        "categorias": Categoria.objects.all() #Busca todas as categorias
    }
    # Renderiza o template index.html com o contexto
    return render(request, 'core/index.html', context)


def lista_produtos(request):
    # Pega o slug da tag da requisição GET
    tag_slug = request.GET.get('tag')

    # Busca todos os produtos publicados
    produtos = Produto.objects.filter(status_produto='published')

    # Se um slug de tag for fornecido, filtra os produtos pela tag
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        produtos = produtos.filter(tags__in=[tag])
    # Busca todos os produtos publicados
    produtos = Produto.objects.filter(status_produto="published")
    # Busca todos os vendedores
    vendedores = Vendedor.objects.all()
    # Calcula a média das avaliações para cada produto

    for p in produtos:
        media_aval = AvaliacaoProduto.objects.filter(produto=p).aggregate(average_classification=Avg('classificacao'))
        if media_aval['average_classification'] is not None:
            p.media_avaliacoes = media_aval['average_classification']
        else:
            p.media_avaliacoes = 0



    # Cria o contexto para o template
    context = {
        "produtos": produtos,
        "vendedores": vendedores,
        "categorias": Categoria.objects.all(), #Busca todas as categorias
        "tags": Tag.objects.all()
    }
    # Renderiza o template product-list.html com o contexto
    return render(request, 'core/product-list.html', context)



def lista_categorias(request):
    # Busca todas as categorias e conta a quantidade de produtos em cada categoria
    categorias = Categoria.objects.all().annotate(produto_count=Count('produtos'))
    # Cria o contexto para o template
    context = {"categorias": categorias}
    # Renderiza o template category-list.html com o contexto
    return render(request, 'core/category-list.html', context)


def categoria_produtos(request, cid):
    # Busca a categoria pelo ID
    categoria = Categoria.objects.get(cid=cid)
    # Busca os produtos publicados que pertencem a categoria
    produtos = Produto.objects.filter(status_produto="published", categoria=categoria)
    # Cria o contexto para o template
    context = {"categoria": categoria, "produtos": produtos}
    # Renderiza o template category-product-list.html com o contexto
    return render(request, "core/category-product-list.html", context)


def lista_vendedores(request):
    # Busca todos os vendedores
    vendedores = Vendedor.objects.all()
    # Cria o contexto para o template, incluindo as categorias
    context = {"vendedores": vendedores, "categorias": Categoria.objects.all()}
    # Renderiza o template vendor-list.html com o contexto
    return render(request, "core/vendor-list.html", context)


def descricao_vendedores(request, vid):
    # Busca o vendedor pelo ID, retorna 404 se não encontrar
    vendedor = get_object_or_404(Vendedor, vid=vid)
    # Busca os produtos publicados do vendedor
    produtos = Produto.objects.filter(vendedor=vendedor, status_produto="published")
    # Busca todas as categorias
    categorias = Categoria.objects.all()
    # Busca todos os vendedores (não parece necessário neste contexto)
    vendedores = Vendedor.objects.all()
    # Cria o contexto para o template
    context = {
        "vendedor": vendedor,
        "produtos": produtos,
        "categorias": categorias,
        "vendedores": vendedores,
    }
    # Renderiza o template vendor-detail.html com o contexto
    return render(request, "core/vendor-detail.html", context)


def detalhes_produto(request, pid):
    # Busca o produto pelo ID, retorna 404 se não encontrar
    produto = get_object_or_404(Produto, pid=pid)
    # Busca produtos da mesma categoria, excluindo o produto atual
    produtos = Produto.objects.filter(categoria=produto.categoria).exclude(pid=pid)
    # Busca todas as categorias
    categorias = Categoria.objects.all()
    # Busca todos os vendedores (não parece necessário neste contexto)
    vendedores = Vendedor.objects.all()
    # Busca as avaliações do produto, ordenadas pela data
    reviews = AvaliacaoProduto.objects.filter(produto=produto).order_by("-data")
    avaliacoes = AvaliacaoProduto.objects.filter(produto=produto)



    # Calcula a média das avaliações
    media_aval = AvaliacaoProduto.objects.filter(produto=produto).aggregate(average_classification=Avg('classificacao'))

    # Cria um formulário de avaliação
    review_form = AvaliacaoProdutoForm()
    # Busca as imagens do produto
    p_imagem = produto.p_imagem.all()

    # Cria o contexto para o template
    context = {
        "p": produto,
        "review_form": review_form,
        "p_imagem": p_imagem,
        "media_aval": media_aval,
        "reviews": reviews,
        "categorias": categorias,
        "vendedores": vendedores,
        "produtos": produtos,
        "avaliacoes": avaliacoes,
    }

    context['range_5'] = range(1, 6)

    # Renderiza o template product-detail.html com o contexto
    return render(request, "core/product-detail.html", context)


def tag_list(request, tag_slug=None):
    # Busca produtos publicados, ordenados pelo ID
    produtos = Produto.objects.filter(status_produto="published").order_by("-id")

    # Inicializa a variável tag como None
    tag = None
    # Se um slug de tag for fornecido
    if tag_slug:
        # Busca a tag pelo slug, retorna 404 se não encontrar
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Filtra os produtos pela tag
        produtos = produtos.filter(tags__in=[tag])

    # Cria o contexto para o template
    context = {
        "produtos": produtos,
        "tag": tag
    }
    # Renderiza o template tag.html com o contexto
    return render(request, "core/tag.html", context)


def ajax_add_review(request, pid):
    # Busca o produto pelo ID, retorna 404 se não encontrar
    produto = get_object_or_404(Produto, pk=pid)
    # Pega o usuário logado
    user = request.user

    # Se o método da requisição for POST
    if request.method == 'POST':
        # Cria um formulário de avaliação com os dados da requisição
        review_form = AvaliacaoProdutoForm(request.POST)
        # Se o formulário for válido
        if review_form.is_valid():
            try:
                # Salva a avaliação, sem commit inicial
                review = review_form.save(commit=False)
                # Define o usuário e o produto da avaliação
                review.user = user
                review.produto = produto
                # Define a data da avaliação
                review.data = timezone.now()
                # Salva a avaliação no banco de dados
                review.save()
                # Retorna uma resposta JSON com sucesso
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
            # Trata exceções
            except ObjectDoesNotExist:
                return JsonResponse({'bool': False, 'errors': 'Usuário ou produto não encontrado'}, status=404)
            except IntegrityError:
                return JsonResponse({'bool': False, 'errors': 'Erro de integridade do banco de dados'}, status=500)
            except ValueError as e:
                return JsonResponse({'bool': False, 'errors': f'Erro de valor: {e}'}, status=500)
            except Exception as e:
                return JsonResponse({'bool': False, 'errors': f'Erro inesperado: {e}'}, status=500)
        # Se o formulário for inválido
        else:
            # Retorna uma resposta JSON com os erros do formulário
            return JsonResponse({'bool': False, 'errors': review_form.errors}, status=400)
    # Se o método da requisição não for POST
    else:
        # Retorna uma resposta JSON indicando método inválido
        return JsonResponse({'bool': False, 'errors': 'Método de requisição inválido'}, status=405)


def search(request):
    # Pega a query de busca da requisição
    query = request.GET.get("q")

    # Busca produtos com o título contendo a query, ordenados pela data
    produtos = Produto.objects.filter(titulo__icontains=query).order_by("-data")

    # Cria o contexto para o template
    context = {
        "produtos": produtos,
        "query": query,
    }
    # Renderiza o template search.html com o contexto
    return render(request, "core/search.html", context)


def filter_product(request):
    categorias = request.GET.getlist("categoria[]")
    vendedores = request.GET.getlist("vendedor[]")

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    produtos = Produto.objects.filter(status_produto="published").order_by("-id").distinct()

    produtos = produtos.filter(preco__gte=min_price)
    produtos = produtos.filter(preco__lte=max_price)

    if len(categorias) > 0:
        produtos = produtos.filter(categoria__id__in=categorias).distinct()


    if len(vendedores) > 0:
        produtos = produtos.filter(vendedor__id__in=vendedores).distinct()


    data = render_to_string("core/async/product-list.html",{"produtos": produtos})
    return JsonResponse({"data": data})


def about(request):
    # Busca produtos publicados e em destaque
    produto = Produto.objects.filter(status_produto="published", destaque=True)
    # Busca todos os vendedores
    vendedores = Vendedor.objects.all()

    context = {
        "produtos": produto,
        "vendedores": vendedores,
        "categorias": Categoria.objects.all() #Busca todas as categorias
    }
    # Renderiza o template index.html com o contexto
    return render(request, 'core/about.html', context)


def privacy_policy(request):
    # Busca produtos publicados e em destaque
    produto = Produto.objects.filter(status_produto="published", destaque=True)
    # Busca todos os vendedores
    vendedores = Vendedor.objects.all()

    context = {
        "produtos": produto,
        "vendedores": vendedores,
        "categorias": Categoria.objects.all() #Busca todas as categorias
    }
    # Renderiza o template index.html com o contexto
    return render(request, 'core/privacy-policy.html', context)


def service_terms(request):
    # Busca produtos publicados e em destaque
    produto = Produto.objects.filter(status_produto="published", destaque=True)
    # Busca todos os vendedores
    vendedores = Vendedor.objects.all()

    context = {
        "produtos": produto,
        "vendedores": vendedores,
        "categorias": Categoria.objects.all() #Busca todas as categorias
    }
    # Renderiza o template index.html com o contexto
    return render(request, 'core/service-terms.html', context)


def add_to_cart(request):
    cart_product = {}
    try:
        product_id = request.GET['id'],
        product_title = request.GET['title'],
        product_qty = int(request.GET['qty']),
        product_price = request.GET['price'],
        product_image = request.GET['image'],
        pid = request.GET['pid'],

    except KeyError as e:
        return JsonResponse({'error': f'Missing parameter: {e}'}, status=400)


    cart_product[str(product_id)] = {
        'title': product_title,
        'qty': product_qty,
        'price': product_price,
        'image': product_image,
        'pid': pid,
    }

    if 'cart_data_obj' in request.session:
        if str(product_id) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(product_id)]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product
    request.session.modified = True
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})
