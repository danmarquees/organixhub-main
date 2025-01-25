from django.shortcuts import render
from core.models import Produto, Categoria, PedidoCarrinho
from django.db.models import Sum
from userauths.models import User
import datetime

# Create your views here.

def dashboard(request):
    revenue = PedidoCarrinho.objects.aggregate(price=Sum("preco"))
    total_orders_count = PedidoCarrinho.objects.count()
    all_products = Produto.objects.all()
    all_categories = Categoria.objects.all()
    new_customers = User.objects.all().order_by("-id")[:5]
    latest_orders = PedidoCarrinho.objects.filter(status_pagamento=True).order_by("-data_pedido")[:5]

    this_month = datetime.datetime.now().month

    monthly_revenue = PedidoCarrinho.objects.filter(data_pedido__month=this_month).aggregate(price=Sum("preco"))

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

def products(request):
    all_products = Produto.objects.all()
    all_categories = Categoria.objects.all()


    context = {
        "all_products": all_products,
        "all_categories": all_categories,
    }
    return render(request, "useradmin/products.html", context)
