from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Categoria, Produto
from .serializers import CategoriaSerializer, ProdutoSerializer

class CategoriaListAPIView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]

class ProdutoDestaqueListAPIView(generics.ListAPIView):
    serializer_class = ProdutoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Baseado na query de produtos destaque que era feita no index via "destaque=True" 
        # ou "em_promocao=True" e status_produto="published"
        return Produto.objects.filter(status_produto="published", destaque=True)

class ProdutoRecenteListAPIView(generics.ListAPIView):
    serializer_class = ProdutoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Baseado em produtos recentes (ordenados por ID/data decrescente)
        return Produto.objects.filter(status_produto="published").order_by('-id')


class ProdutoListAPIView(generics.ListAPIView):
    serializer_class = ProdutoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Permite retornar todos os produtos publicados
        return Produto.objects.filter(status_produto="published")

from django.http import JsonResponse

def get_cart_data(request):
    cart_total_amount = 0
    cart_data_formatted = {}

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            qty = int(item['qty'])
            price = float(item['price'])
            subtotal = qty * price
            cart_total_amount += subtotal
            cart_data_formatted[p_id] = {
                'title': item['title'],
                'qty': qty,
                'price': price,
                'image': item['image'],
                'pid': item['pid'],
                'subtotal': subtotal
            }

    return JsonResponse({
        "cart_data": cart_data_formatted,
        "totalcartitems": len(request.session.get('cart_data_obj', {})),
        "cart_total_amount": cart_total_amount
    })
