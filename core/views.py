from django.db.models.aggregates import Avg  # Importa a função Avg para calcular a média
from django.http import JsonResponse # Importa JsonResponse para retornar respostas JSON
from django.shortcuts import HttpResponse, render, get_object_or_404, redirect # Importa funções para renderizar templates e lidar com requisições
from django.db.models import Count # Importa funções para contagem e agregação de dados
from taggit.models import Tag # Importa o modelo Tag para lidar com tags
from core.models import Produto, Categoria, Vendedor, PedidoCarrinho, ItensPedidoCarrinho, Wishlist, AvaliacaoProduto, Endereco, Coupon # Importa modelos do aplicativo core
from core.forms import AvaliacaoProdutoForm # Importa o formulário para avaliações de produtos
from userauths.models import Profile, Contato # Importa o modelo de usuário
from django.utils import timezone # Importa funções relacionadas a data e hora
from django.template.loader import render_to_string # Importa a função render_to_string para renderizar templates a partir de strings.
from django.contrib import messages # Importa o módulo messages para exibir mensagens de feedback ao usuário.
from decimal import Decimal # Importa a classe Decimal para realizar cálculos de precisão arbitrária com números decimais.
from django.urls import reverse # Importa a função reverse para gerar URLs com base nos nomes das views.
from django.conf import settings # Importa o módulo settings para acessar as configurações do projeto.
from django.views.decorators.csrf import csrf_exempt # Importa o decorator csrf_exempt para desabilitar a verificação de CSRF em views específicas.
from django.contrib.auth.decorators import login_required # Importa o decorator login_required para restringir o acesso a views apenas a usuários autenticados.
from paypal.standard.forms import PayPalPaymentsForm # Importa a classe PayPalPaymentsForm para gerar formulários de pagamento do PayPal.
from django.http import HttpResponseNotFound # Importa a classe HttpResponseNotFound para retornar uma resposta HTTP 404 (Not Found).
from django.core.exceptions import ValidationError # Importa a classe ValidationError para lidar com exceções de validação de dados.
from django.db import IntegrityError # Importa a classe IntegrityError para lidar com exceções de integridade do banco de dados.
from brazilcep import get_address_from_cep, WebService # Importa funções da biblioteca brazilcep para buscar informações de endereço a partir de CEPs.
import calendar # Importa o módulo calendar para trabalhar com datas e calendários.
from django.db.models.functions import ExtractMonth # Importa a função ExtractMonth para extrair o mês de um campo de data.
from paypal.standard.ipn.forms import PayPalIPNForm # Importa a classe PayPalIPNForm para processar notificações instantâneas de pagamento (IPN) do PayPal.
import stripe
from paypal.standard.forms import PayPalPaymentsForm
from core import models
from django.db.models import Q


def index(request):
    produtos = Produto.objects.filter(status_produto="published", destaque=True)
    vendedores = Vendedor.objects.all()
    categorias = Categoria.objects.all().annotate(produto_count=Count('categoria'))

    for p in produtos:
        media_aval = AvaliacaoProduto.objects.filter(produto=p).aggregate(average_classification=Avg('classificacao'))
        if media_aval['average_classification'] is not None:
            p.media_avaliacoes = media_aval['average_classification']
        else:
            p.media_avaliacoes = 0


        #Corrected String Splitting for SQLite
        p.badges = list(p.badges) if p.badges is not None else []


    context = {
        "produtos": produtos,
        "vendedores": vendedores,
        "categorias": categorias,
    }
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
    if request.user.is_authenticated:
        try:
            endereco = Endereco.objects.get(user=request.user, status=False)
        except Endereco.DoesNotExist:
            endereco = None  # Ou algum valor padrão
    else:
        endereco = None
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
        "endereco": endereco,
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



import logging

logger = logging.getLogger(__name__)
@login_required
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

                average_rating = AvaliacaoProduto.objects.filter(produto=produto).aggregate(Avg('classificacao'))['classificacao__avg']
                formatted_average = "{:.1f}".format(average_rating) if average_rating is not None else "0.0"

                return JsonResponse({
                    'bool': True,
                    'context': {
                        'user': user.username,
                        'review': review.avaliacao,
                        'rating': review.classificacao,
                        'data': review.data.strftime("%d %b, %Y"),
                        'user_image': user.profile.imagem.url if hasattr(user, 'profile') and user.profile.imagem else None,
                        'average_rating': formatted_average,
                    },
                })
            except IntegrityError:
                return JsonResponse({'bool': False, 'errors': 'Erro de integridade do banco de dados'}, status=500)
            except Exception as e:
                logger.exception(e)  # Loga a exceção com traceback completo
                return JsonResponse({'bool': False, 'errors': 'Ocorreu um erro ao processar sua avaliação.'}, status=500)

        else:
            return JsonResponse({'bool': False, 'errors': review_form.errors}, status=400)
    else:
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
    # Inicializa variáveis
    cart_total_amount = Decimal('0.00')
    errors = []
    cart_data = request.session.get('cart_data_obj', {})  # Obtém o carrinho da sessão
    cart_data_formatted = {}

    # Processa os itens no carrinho para cálculo do total
    for p_id, item in cart_data.items():
        try:
            qty = int(item['qty'])
            price = Decimal(str(item['price']))
            if qty <= 0 or price <= 0:
                errors.append(f"Item inválido: {item.get('title', 'desconhecido')}")
                continue  # Ignora itens inválidos
            subtotal = qty * price
            cart_total_amount += subtotal
            cart_data_formatted[p_id] = {
                'title': item['title'],
                'qty': qty,
                'price': "{:.2f}".format(price),
                'image': item['image'],
                'pid': item['pid'],
                'subtotal': "{:.2f}".format(subtotal),
            }
        except (ValueError, TypeError, KeyError) as e:
            errors.append(f"Erro ao processar item {item.get('title', 'desconhecido')}: {e}")

    # Busca ou cria o pedido atual do usuário
    try:
        order = PedidoCarrinho.objects.filter(user=request.user, status_pagamento=False).order_by('-data_pedido').first()
        if not order:
            order = PedidoCarrinho.objects.create(
                user=request.user,
                nome=request.POST.get('nome'),
                email=request.POST.get('email'),
                telefone=request.POST.get('telefone'),
                endereco=request.POST.get('endereco'),
                cidade=request.POST.get('cidade'),
                estado=request.POST.get('estado'),
                preco=cart_total_amount,
                status_pagamento=False,
                data_pedido=timezone.now(),
            )
            # Adiciona os itens do carrinho ao pedido
            for product_id, item in cart_data.items():
                try:
                    produto = models.Produto.objects.get(pk=product_id)
                    models.ItensPedidoCarrinho.objects.create(
                        pedido=order,
                        num_fatura=order.num_fatura,
                        status_produto=order.status_produto,
                        item=item['title'],
                        imagem=item['image'],
                        qtd=item['qty'],
                        preco=item['price'],
                        total=item['price'] * item['qty'],
                    )
                except models.Produto.DoesNotExist:
                    errors.append(f"Produto com ID {product_id} não encontrado.")
    except Exception as e:
        errors.append(f"Erro ao buscar ou criar pedido: {str(e)}")
        order = None

    # Aplicação de cupom
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        if not codigo:
            messages.warning(request, "Por favor, insira um código de cupom.")
            return redirect("core:checkout")
        try:
            coupon = models.Coupon.objects.get(codigo=codigo, ativo=True)
            if order: #check if order exists before applying coupon
                order.apply_coupon(coupon)  # Aplica o cupom ao pedido
            messages.success(request, f"Cupom '{codigo}' aplicado com sucesso!")
        except models.Coupon.DoesNotExist:
            messages.warning(request, "Cupom inválido ou inativo.")
        except ValueError as ve:
            messages.warning(request, str(ve))
        except Exception as e:
            messages.error(request, f"Erro ao aplicar cupom: {str(e)}")
        return redirect("core:checkout")

    # Configurações do PayPal
    final_amount = cart_total_amount #added this line to solve undefined variable error


    # Contexto para o template
    context = {
        "cart_data": cart_data_formatted,
        "totalcartitems": len(cart_data),
        "cart_total_amount": "{:.2f}".format(cart_total_amount),
        "final_amount": "{:.2f}".format(final_amount),
        "order": order,
        "errors": errors,
    }

    return render(request, "core/checkout.html", context)



import uuid
import logging

logger = logging.getLogger(__name__)
@login_required
def pagamento_efetuado(request):
    # Verifica se há dados de carrinho na sessão
    if 'cart_data_obj' in request.session:
        # Obtém os dados do carrinho
        cart_data = request.session['cart_data_obj']
        # Busca ou cria o pedido atual do usuário
        try:
            order = PedidoCarrinho.objects.filter(user=request.user, status_pagamento=False).order_by('-data_pedido').first()
            if not order:
                order = PedidoCarrinho.objects.create(
                    user=request.user,
                    nome=request.POST.get('nome'),
                    email=request.POST.get('email'),
                    telefone=request.POST.get('telefone'),
                    endereco=request.POST.get('endereco'),
                    cidade=request.POST.get('cidade'),
                    estado=request.POST.get('estado'),
                    preco=Decimal('0.00'),  # Initialize price to zero
                    status_pagamento=True,  # Set payment status to True
                    data_pedido=timezone.now(),
                    payment_date=timezone.now() #Set payment date
                )
                # Adiciona os itens do carrinho ao pedido
                for product_id, item in cart_data.items():
                    try:
                        produto = models.Produto.objects.get(pk=product_id)
                        models.ItensPedidoCarrinho.objects.create(
                            pedido=order,
                            num_fatura=order.num_fatura,
                            status_produto=order.status_produto,
                            item=item['title'],
                            imagem=item['image'],
                            qtd=item['qty'],
                            preco=item['price'],
                            total=item['price'] * item['qty'],
                        )
                    except models.Produto.DoesNotExist:
                        print(f"Produto com ID {product_id} não encontrado.")  # Handle missing products gracefully

            # Limpa os dados do carrinho da sessão
            del request.session['cart_data_obj']
            request.session.modified = True

        except Exception as e:
            print(f"Erro ao criar pedido: {e}")  # Log the error
            # Handle the error appropriately, e.g., display an error message to the user
            return render(request, 'core/payment-failed.html', {'error_message': 'Ocorreu um erro ao processar seu pagamento. Por favor, tente novamente.'})


    # Renderiza o template de pagamento concluído
    return render(request, 'core/payment-completed.html')

@login_required
def save_checkout_info(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        try:
            order = PedidoCarrinho.objects.filter(user=request.user, status_pagamento=False).order_by('-data_pedido').first()
            if not order:
                order = PedidoCarrinho.objects.create(
                    user=request.user,
                    nome=nome,
                    email=email,
                    telefone=telefone,
                    endereco=endereco,
                    cidade=cidade,
                    estado=estado,
                    preco=Decimal('0.00'), # Initialize price to zero
                    status_pagamento=False,
                    data_pedido=timezone.now(),
                )
            else:
                order.nome = nome
                order.email = email
                order.telefone = telefone
                order.endereco = endereco
                order.cidade = cidade
                order.estado = estado
                order.save()
            return JsonResponse({'success': True, 'message': 'Informações de checkout salvas com sucesso!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro ao salvar informações de checkout: {str(e)}'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Método de requisição inválido'}, status=405)


@login_required
def pagamento_falha(request):
    return render(request, 'core/payment-failed.html')



import logging

logger = logging.getLogger(__name__)

@login_required
def customer_dashboard(request):
    orders_list = PedidoCarrinho.objects.filter(user=request.user).order_by("-id")
    addresses = Endereco.objects.filter(user=request.user).order_by("-id")
    profile = Profile.objects.get(user=request.user)

    orders = PedidoCarrinho.objects.annotate(month=ExtractMonth("data_pedido")).values("month").annotate(count=Count("id")).values("month", "count")
    meses_pt = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    month = []
    total_orders = []

    for o in orders:
        month.append(meses_pt[o['month']])
        total_orders.append(o["count"])


    if request.method == "POST":
        try:
            num_addresses = int(request.POST.get('num_addresses', 1))
            created_addresses = []
            for i in range(num_addresses):
                address_data = {
                    'cep': request.POST.get(f'cep_{i}', '').strip(),
                    'logradouro': request.POST.get(f'logradouro_{i}', '').strip(),
                    'complemento': request.POST.get(f'complemento_{i}', '').strip(),
                    'bairro': request.POST.get(f'bairro_{i}', '').strip(),
                    'localidade': request.POST.get(f'localidade_{i}', '').strip(),
                    'uf': request.POST.get(f'uf_{i}', '').strip(),
                    'numero': request.POST.get(f'numero_{i}', '').strip(),
                    'celular': request.POST.get(f'celular_{i}', '').strip(),
                    'user': request.user,
                    'status': False,
                }
                new_address = Endereco(**address_data)
                new_address.full_clean()  # This will raise ValidationError if any errors
                new_address.save()
                created_addresses.append(new_address)
                logger.info(f"Endereço criado com sucesso: {new_address.id}")

            messages.success(request, f"{len(created_addresses)} endereços adicionados com sucesso!")
        except ValueError as e:
            messages.error(request, f"Erro de valor: {e}")
            logger.exception(f"ValueError ao criar endereços: {e}")
        except IntegrityError as e:
            messages.error(request, "Erro de integridade no banco de dados. Verifique os dados e tente novamente.")
            logger.exception(f"IntegrityError: {e}")
        except ValidationError as e:
            error_messages = []
            for field, errors in e.message_dict.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            messages.error(request, "Erro de validação: " + ", ".join(error_messages))
            logger.exception(f"ValidationError: {e}")
        except Exception as e:
            messages.error(request, "Ocorreu um erro inesperado. Tente novamente.")
            logger.exception(f"Erro inesperado: {e}")

        return redirect('core:dashboard') # Redirect back to the dashboard after POST

    context = {
        "orders_list": orders_list,
        "addresses": addresses,
        "profile": profile,
        "orders": orders,
        "month": month,
        "total_orders": total_orders,
    }
    return render(request, 'core/dashboard.html', context)


def order_detail(request, id):
    try:
        order = get_object_or_404(PedidoCarrinho, user=request.user, id=id)
        order_items = order.itenspedidocarrinho_set.all() # Accessing related objects using the reverse relation

        context = {
            "order": order,
            "order_items": order_items,
        }
        return render(request, 'core/order-detail.html', context)
    except PedidoCarrinho.DoesNotExist:
        logger.warning(f"Order with id {id} not found for user {request.user.id}")
        return HttpResponseNotFound("Pedido não encontrado.")
    except Exception as e:
        logger.exception(f"An error occurred while retrieving order details: {e}")
        return HttpResponseNotFound("Ocorreu um erro.")


def make_address_default(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id')
            if id is None:
                return JsonResponse({"success": False, "error": "Missing 'id' parameter"}, status=400)
            try:
                id = int(id)
            except ValueError:
                return JsonResponse({"success": False, "error": "Invalid 'id' parameter"}, status=400)

            user = request.user

            try:
                address = Endereco.objects.get(pk=id, user=user)
                # Only one address can be default, so set all others to False first
                Endereco.objects.filter(user=user, status=True).update(status=False)
                address.status = True
                address.save()
                return JsonResponse({"success": True})
            except Endereco.DoesNotExist:
                return JsonResponse({"success": False, "error": "Address not found"}, status=404)
            except Exception as e:
                return JsonResponse({"success": False, "error": f"An unexpected error occurred: {e}"}, status=500)

        except Exception as e:
            return JsonResponse({"success": False, "error": f"An unexpected error occurred: {e}"}, status=500)
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

@login_required
def delete_address(request):
    if request.method == 'POST':
        try:
            address_id = request.POST.get('id')
            if address_id is None:
                return JsonResponse({"success": False, "error": "Missing 'id' parameter"}, status=400)
            try:
                address_id = int(address_id)
            except ValueError:
                return JsonResponse({"success": False, "error": "Invalid 'id' parameter"}, status=400)

            address = get_object_or_404(Endereco, pk=address_id, user=request.user)
            address.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": f"An unexpected error occurred: {e}"}, status=500)
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

def buscar_endereco(request):
    cep = request.GET.get('cep', '').replace('-', '').strip()

    if len(cep) != 8 or not cep.isdigit():
        return JsonResponse({'erro': 'CEP inválido!'}, status=400)

    try:
        endereco = get_address_from_cep(cep, webservice=WebService.VIACEP)
        return JsonResponse(endereco)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


def product_quickview(request, pid):
    if request.method == 'GET':
        try:
            produto = get_object_or_404(Produto, pid=pid)
            p_imagem = produto.p_imagem.all()

            # Prepare os dados do produto
            context = {
                'p_imagem': p_imagem,
                'pid': produto.pid,
                'titulo': produto.titulo,
                'preco': str(produto.preco),
                'preco_antigo': str(produto.preco_antigo),
                'descricao': produto.descricao,
                'imagem': produto.imagem.url if produto.imagem else None,
                'vendedor': produto.vendedor.titulo if produto.vendedor else None,
                'categoria': produto.categoria.titulo if produto.categoria else None,
                'em_estoque': produto.em_estoque,
                'qtd_estoque': produto.qtd_estoque,
                'porcentagem_desconto': produto.obter_porcentagem(),
            }
            return JsonResponse(context)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user) #Filtro pelo usuario logado
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    context = {
        "wishlist_items": wishlist_items, # Corrigido para usar o nome correto da variável
        "wishlist_count": wishlist_count
    }
    return render(request, 'core/wishlist.html', context)



def add_to_wishlist(request):
    if request.method == 'GET':
        try:
            product_id = request.GET['id']
            product = get_object_or_404(Produto, pk=product_id)
            user = request.user

            wishlist_count = Wishlist.objects.filter(produto=product, user=user).count() #Corrected
            if wishlist_count > 0:
                return JsonResponse({"bool": False, "message": "Produto já adicionado à lista de desejos."})
            else:
                Wishlist.objects.create(produto=product, user=user) #Corrected
                return JsonResponse({"bool": True, "message": "Produto adicionado à lista de desejos com sucesso!"})
        except KeyError:
            return JsonResponse({"bool": False, "message": "Parâmetro 'id' ausente."}, status=400)
        except Exception as e:
            return JsonResponse({"bool": False, "message": f"Erro ao adicionar à lista de desejos: {e}"}, status=500)
    else:
        return JsonResponse({"bool": False, "message": "Método de requisição inválido."}, status=405)


@csrf_exempt
@login_required
def delete_wishlist_item(request):
    if request.method != 'POST':
        return JsonResponse({"bool": False, "message": "Método de requisição inválido."}, status=405)

    try:
        pid = request.POST['id']
        try:
            product = get_object_or_404(Wishlist, pk=pid, user=request.user)
            product.delete()
            logger.info(f"Item da Wishlist deletado com sucesso (ID: {pid}, Usuário: {request.user.id})")
            wishlist_items = Wishlist.objects.filter(user=request.user)
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
            context = {
                "wishlist_items": wishlist_items,
                "wishlist_count": wishlist_count
            }
            html = render_to_string('core/async/wishlist-list.html', context)
            return JsonResponse({"bool": True, "message": "Item deletado da lista de desejos com sucesso!", "html": html})
        except Wishlist.DoesNotExist:
            return JsonResponse({"bool": False, "message": "Item da Wishlist não encontrado."}, status=404)
        except IntegrityError as e:
            logger.exception(f"Erro de integridade ao deletar item da Wishlist (ID: {pid}, Usuário: {request.user.id}): {e}")
            return JsonResponse({"bool": False, "message": "Erro de integridade do banco de dados. Por favor, tente novamente mais tarde."}, status=500)
        except Exception as e:
            logger.exception(f"Erro inesperado ao deletar item da Wishlist (Usuário: {request.user.id}): {e}")
            return JsonResponse({"bool": False, "message": f"Erro ao remover da lista de desejos: {e}"}, status=500)

    except KeyError:
        logger.warning(f"Parâmetro 'id' ausente na requisição de exclusão de item da Wishlist do usuário: {request.user.id}")
        return JsonResponse({"bool": False, "message": "Parâmetro 'id' ausente."}, status=400)



def contact(request):
    return render(request, 'core/contact.html')


def ajax_contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')

        try:
            Contato.objects.create(
                nome=nome,
                email=email,
                telefone=telefone,
                assunto=assunto,
                mensagem=mensagem
            )
            return JsonResponse({"success": True, "message": "Mensagem enviada com sucesso!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Erro ao enviar mensagem: {str(e)}"}, status=500)

    else:
        return JsonResponse({"success": False, "message": "Método de requisição inválido."}, status=405)


def purchase_guide(request):
    return render(request, "core/purchase-guide.html")
