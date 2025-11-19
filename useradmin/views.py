from django.shortcuts import render, redirect, get_object_or_404
from core.models import Produto, Categoria, PedidoCarrinho
from django.db.models import Sum
from userauths.models import User
import datetime
from useradmin.forms import AddProductForm
from core.models import ItensPedidoCarrinho, AvaliacaoProduto
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.

@login_required
def dashboard(request):
    revenue = PedidoCarrinho.objects.filter(status_pagamento=True).aggregate(price=Sum("preco"))
    total_orders_count = PedidoCarrinho.objects.filter(status_pagamento=True).count()
    all_products = Produto.objects.all()
    all_categories = Categoria.objects.all()
    new_customers = User.objects.all().order_by("-id")[:5]
    latest_orders = PedidoCarrinho.objects.filter(status_pagamento=True).order_by("-data_pedido")[:5]

    this_month = datetime.datetime.now().month

    monthly_revenue = PedidoCarrinho.objects.filter(status_pagamento=True, data_pedido__month=this_month).aggregate(price=Sum("preco"))

    context = {
        "revenue": revenue,
        "total_orders_count": total_orders_count,
        "all_products": all_products,
        "all_categories": all_categories,
        "new_customers": new_customers,
        "latest_orders": latest_orders,
        "monthly_revenue": monthly_revenue,
    }
    return render(request, "useradmin/dashboard.html", context)

@login_required
def products(request):
    all_products = Produto.objects.all().order_by("-id")
    all_categories = Categoria.objects.all()


    context = {
        "all_products": all_products,
        "all_categories": all_categories,
    }
    return render(request, "useradmin/products.html", context)


@login_required
def add_product(request):
    if request.method == "POST":
       form = AddProductForm(request.POST, request.FILES)
       if form.is_valid():
           new_form = form.save(commit=False)
           new_form.user = request.user
           new_form.save()
           form.save_m2m()
           return redirect("useradmin:dashboard")
    else:
        form = AddProductForm()

    context = {
        "form": form
    }

    return render(request, "useradmin/add-product.html", context)


@login_required
def edit_product(request, pid):
    product = get_object_or_404(Produto, pid=pid)
    if request.method == "POST":
       form = AddProductForm(request.POST, request.FILES, instance=product)
       if form.is_valid():
           new_form = form.save(commit=False)
           new_form.user = request.user
           new_form.save()
           form.save_m2m()
           return redirect("useradmin:edit-product", product.pid)
    else:
        form = AddProductForm(instance=product)

    context = {
        "form": form,
        "product": product
    }

    return render(request, "useradmin/edit-product.html", context)


@login_required
@require_POST
def delete_product(request, pid):
    product = get_object_or_404(Produto, pid=pid)
    product.delete()
    return redirect("useradmin:products")


@login_required
def orders(request):
    orders = PedidoCarrinho.objects.all()
    context = {
        "orders": orders,
    }

    return render(request, "useradmin/orders.html", context)


@login_required
def order_detail(request, id):
    order = get_object_or_404(PedidoCarrinho, orderid=id)
    order_items = ItensPedidoCarrinho.objects.filter(pedido=order)

    context = {
        "order": order,
        "order_items": order_items,
    }

    return render(request, "useradmin/order-detail.html", context)


@login_required
def change_order_status(request, id):
    try:
        order = get_object_or_404(PedidoCarrinho, orderid=id)
    except Exception:
        messages.error(request, "Pedido não encontrado.")
        return redirect('useradmin:orders')

    if request.method == 'POST':
        status = request.POST.get("status")

        if status in dict(PedidoCarrinho._meta.get_field('status_produto').choices):
            order.status_produto = status
            order.save()
            messages.success(request, f"Status do Pedido Alterado para {order.get_status_produto_display()}")
        else:
            messages.error(request, "Status inválido. Por favor, selecione um status da lista.")
            return redirect('useradmin:order_detail', id)

    return redirect('useradmin:order-detail', id)


@login_required
def shop_page(request):
    products = Produto.objects.all()
    revenue = PedidoCarrinho.objects.filter(status_pagamento=True).aggregate(price=Sum("preco"))
    total_sales = ItensPedidoCarrinho.objects.filter(pedido__status_produto=True).aggregate(qtd=Sum("qtd"))

    context = {
        "products": products,
        "revenue": revenue,
        "total_sales": total_sales,
    }

    return render(request, "useradmin/shop-page.html", context)



@login_required
def reviews(request):
    reviews = AvaliacaoProduto.objects.all()

    context = {
        "reviews": reviews,
    }

    return render(request, "useradmin/reviews.html", context)
