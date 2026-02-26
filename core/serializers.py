from rest_framework import serializers
from .models import Categoria, Produto, Vendedor

class CategoriaSerializer(serializers.ModelSerializer):
    produto_count = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ['cid', 'titulo', 'imagem', 'produto_count']

    def get_produto_count(self, obj):
        # We assume the related_name on Produto is 'categoria'
        return obj.categoria.count()


class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ['vid', 'titulo', 'imagem', 'reputacao']


class ProdutoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()
    vendedor = VendedorSerializer()
    obter_porcentagem = serializers.SerializerMethodField()
    badges = serializers.SerializerMethodField()
    fim_promocao_timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = [
            'id', 'pid', 'titulo', 'imagem', 'preco', 'preco_antigo', 
            'categoria', 'vendedor', 'qtd_estoque', 'qtd_vendida', 
            'obter_porcentagem', 'badges', 'fim_promocao', 'fim_promocao_timestamp'
        ]

    def get_obter_porcentagem(self, obj):
        return obj.obter_porcentagem()

    def get_badges(self, obj):
        return obj.get_badges()
    
    def get_fim_promocao_timestamp(self, obj):
        if obj.fim_promocao:
            return obj.fim_promocao.timestamp()
        return None
