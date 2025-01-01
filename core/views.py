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
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm




def index(request):
    # Busca produtos publicados e em destaque
    produtos = Produto.objects.filter(status_produto="published", destaque=True)
    # Busca todos os vendedores
    vendedores = Vendedor.objects.all()
    categorias = Categoria.objects.all().annotate(produto_count=Count('categoria'))
    # Cria o contexto para o template


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
        "categorias": categorias,
        #Busca todas as categorias
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
    categorias = Categoria.objects.all().annotate(produto_count=Count('categoria'))
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

    categorias = Categoria.objects.all().annotate(produto_count=Count('categoria'))



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
    try:
        product_id = request.GET['id']
        product_title = request.GET['title']
        product_qty = int(request.GET['qty'])
        product_price_str = request.GET['price'] # Recebe o preço como string
        product_price = float(product_price_str.replace(',', '.')) # Converte para float APÓS substituir a vírgula

        product_image = request.GET['image']
        pid = request.GET['pid']

        if product_qty <= 0:
            return JsonResponse({'error': 'Quantidade deve ser maior que zero'}, status=400)

    except KeyError as e:
        return JsonResponse({'error': f'Missing parameter: {e}'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': f'Preço inválido: {e}'}, status=400) # Mensagem de erro mais informativa


    cart_item = {
        'title': product_title,
        'qty': product_qty,
        'price': product_price,
        'image': product_image,
        'pid': pid,
    }

    cart = request.session.get('cart_data_obj', {})

    if str(product_id) in cart:
        cart[str(product_id)]['qty'] += product_qty
    else:
        cart[str(product_id)] = cart_item

    request.session['cart_data_obj'] = cart
    request.session.modified = True

    return JsonResponse({"data": cart, 'totalcartitems': len(cart)})

import logging

logger = logging.getLogger(__name__)

def cart_view(request):
    cart_total_amount = 0
    cart_data_formatted = {}
    errors = [] # Lista para armazenar mensagens de erro

    if 'cart_data_obj' in request.session:
        print(f"Cart data from session: {request.session['cart_data_obj']}")

        for p_id, item in request.session['cart_data_obj'].items():
            try:
                qty = int(item['qty'])
                price = float(item['price'])
                if qty <= 0 or price <= 0:
                    errors.append(f"Invalid quantity or price for item {item['title']}.")
                    continue # Pula para o próximo item se houver um erro

                subtotal = qty * price
                cart_total_amount += subtotal
                cart_data_formatted[p_id] = {
                    'title': item['title'],
                    'qty': qty,
                    'price': "{:.2f}".format(price),
                    'image': item['image'],
                    'pid': item['pid'],
                    'subtotal': "{:.2f}".format(subtotal)
                }
            except (ValueError, TypeError) as e:
                errors.append(f"Error processing item {item.get('title', 'unknown')}: {e}")
            except KeyError as e:
                errors.append(f"Missing key '{e}' in cart item {item.get('title', 'unknown')}.")

        # Exibe a página do carrinho, mesmo com erros
        return render(request, "core/cart.html", {
            "cart_data": cart_data_formatted,
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': "{:.2f}".format(cart_total_amount),
            'errors': errors, # Passa a lista de erros para o template
        })
    else:
        messages.warning(request, "Seu Carrinho Está Vazio.")
        return redirect("core:index")


def delete_item_from_cart(request):
    product_id = str(request.GET.get('id'))
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            del request.session['cart_data_obj'][product_id]
            request.session.modified = True

            # Recalculate cart totals and format data for the template
            cart_total_amount = 0
            cart_data_formatted = {}
            for p_id, item in request.session.get('cart_data_obj', {}).items():
                try:
                    qty = int(item['qty'])
                    price = float(item['price'])
                    if qty <= 0 or price <= 0:
                        continue  # Skip items with invalid quantity or price

                    subtotal = qty * price
                    cart_total_amount += subtotal
                    cart_data_formatted[p_id] = {
                        'title': item['title'],
                        'qty': qty,
                        'price': "{:.2f}".format(price),
                        'image': item['image'],
                        'pid': item['pid'],
                        'subtotal': "{:.2f}".format(subtotal)
                    }
                except (ValueError, TypeError, KeyError) as e:
                    print(f"Error processing cart item {item}: {e}") # Log the error
                    pass  # Handle errors gracefully

            context = {
                "cart_data": cart_data_formatted,
                'totalcartitems': len(request.session.get('cart_data_obj', {})),
                'cart_total_amount': "{:.2f}".format(cart_total_amount),
                'errors': []
            }
            return JsonResponse({"data": render_to_string("core/async/cart-list.html", context), 'totalcartitems': len(request.session.get('cart_data_obj',{}))})

        else:
            return JsonResponse({"error": "Product not found in cart."}, status=404)
    else:
        return JsonResponse({"error": "Cart is empty."}, status=404)


import logging
logger = logging.getLogger(__name__)
def update_from_cart(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        product_id = request.POST['id']
        quantity = int(request.POST['quantity'])
        if quantity <= 0:
            return JsonResponse({'error': 'Quantity must be greater than zero'}, status=400)

    except (KeyError, ValueError) as e:
        return JsonResponse({'error': f'Invalid request data: {str(e)}'}, status=400)

    if 'cart_data_obj' not in request.session:
        return JsonResponse({'error': 'Cart is empty'}, status=404)

    cart_data = request.session['cart_data_obj']
    if product_id not in cart_data:
        return JsonResponse({'error': 'Product not found in cart'}, status=404)

    try:
        cart_data[product_id]['qty'] = quantity

        # Convert Decimal values to float WITHIN cart_data
        for p_id, item in cart_data.items():
            if 'price' in item and isinstance(item['price'], Decimal):
                item['price'] = float(item['price'])
            if 'subtotal' in item and isinstance(item['subtotal'], Decimal):
                item['subtotal'] = float(item['subtotal'])

        request.session['cart_data_obj'] = cart_data
        request.session.modified = True

        cart_total_amount = 0.0 # Initialize as float
        for p_id, item in cart_data.items():
            qty = int(item.get('qty', 0))
            price = float(item.get('price', 0))
            if qty > 0 and price > 0:
                subtotal = qty * price
                cart_total_amount += subtotal # += works with floats

        updated_product = cart_data[product_id]
        product_subtotal = updated_product['qty'] * updated_product['price']

        return JsonResponse({
            "totalcartitems": len(cart_data),
            "cart_total_amount": cart_total_amount,
            "subtotal": product_subtotal,
            "product_id": product_id,
            "quantity": quantity,
            "errors": []
        })

    except (KeyError, ValueError, TypeError) as e:
        logger.exception(f"Error updating cart: {e}")
        return JsonResponse({'error': f'Error updating cart: {e}'}, status=500)
    except Exception as e:
        logger.exception(f"Error updating cart: {e}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)




@login_required
def checkout(request):
    host = request.get_host()
    cart_total_amount = 0.0  # Initialize as float
    cart_data = request.session.get('cart_data_obj', {})
    errors = []  # Lista para armazenar mensagens de erro
    cart_data_formatted = {}
    for p_id, item in cart_data.items():
        try:
            qty = int(item['qty'])
            price = float(item['price'])
            if qty <= 0 or price <= 0:
                errors.append(f"Invalid quantity or price for item {item['title']}.")
                continue  # Pula para o próximo item se houver um erro

            subtotal = qty * price
            cart_total_amount += subtotal
            cart_data_formatted[p_id] = {
                'title': item['title'],
                'qty': qty,
                'price': "{:.2f}".format(price),
                'image': item['image'],
                'pid': item['pid'],
                'subtotal': "{:.2f}".format(subtotal)
            }
        except (ValueError, TypeError) as e:
            errors.append(f"Error processing item {item.get('title', 'unknown')}: {e}")
        except KeyError as e:
            errors.append(f"Missing key '{e}' in cart item {item.get('title', 'unknown')}.")

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': "{:.2f}".format(cart_total_amount), # Use cart total amount
        'item_name': "Order",
        'invoice': "INVOICE-{}".format(request.user.id), # more dynamic invoice
        'currency_code': "BRL",
        'notify_url': 'http://{}{}'.format(host, reverse("core:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("core:payment-completed")),
        'cancel_url': 'http://{}{}'.format(host, reverse("core:payment-failed")),
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, "core/checkout.html", {
        "cart_data": cart_data_formatted,
        'totalcartitems': len(cart_data),
        'cart_total_amount': "{:.2f}".format(cart_total_amount),
        'errors': errors, # Passa a lista de erros para o template
        'paypal_payment_button': paypal_payment_button, # Include the button
    })


@login_required
def pagamento_efetuado(request):
    cart_data = request.session.get('cart_data_obj', {})
    cart_total_amount = 0.0
    cart_data_formatted = {}
    errors = []
    for p_id, item in cart_data.items():
        try:
            qty = int(item['qty'])
            price = float(item['price'])
            if qty <= 0 or price <= 0:
                errors.append(f"Invalid quantity or price for item {item['title']}.")
                continue
            subtotal = qty * price
            cart_total_amount += subtotal
            cart_data_formatted[p_id] = {
                'title': item['title'],
                'qty': qty,
                'price': "{:.2f}".format(price),
                'image': item['image'],
                'pid': item['pid'],
                'subtotal': "{:.2f}".format(subtotal)
            }
        except (ValueError, TypeError, KeyError) as e:
            errors.append(f"Error processing item {item.get('title', 'unknown')}: {e}")

    return render(request, 'core/payment-completed.html', {
        "cart_data": cart_data_formatted,
        'totalcartitems': len(cart_data),
        'cart_total_amount': "{:.2f}".format(cart_total_amount),
        'errors': errors,
    })



def pagamento_falha(request):
    return render(request, 'core/payment-failed.html')
