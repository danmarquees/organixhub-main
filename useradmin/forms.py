from core.models import Produto
from django import forms


class AddProductForm(forms.ModelForm):
    model = Produto
    fields = [
        'titulo',
        'imagem',
        'descricao',
        'preco',
        'preco_antigo',
        'especificacoes',
        'tipo',
        'qtd_estoque',
        'validade',
        'data_fab',
        'digital',
        'categoria',
    ]
