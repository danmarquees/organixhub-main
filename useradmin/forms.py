from core.models import Produto
from django import forms


class AddProductForm(forms.ModelForm):
    titulo = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Título do produto", "class": "form-control"}))
    descricao = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Descrição", "class": "form-control"}))
    preco = forms.DecimalField(widget=forms.TextInput(attrs={"placeholder": "Preço", "class": "form-control"}))
    preco_antigo = forms.DecimalField(widget=forms.TextInput(attrs={"placeholder": "Preço antigo", "class": "form-control"}))
    tipo = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Tipo", "class": "form-control"}))
    qtd_estoque = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": "Quantidade disponível em estoque", "class": "form-control"}))
    validade = forms.DateField(widget=forms.DateInput(attrs={"placeholder": "Validade", "class": "form-control"}))
    data_fab = forms.DateField(widget=forms.DateInput(attrs={"placeholder": "e.g: 25-01-23", "class": "form-control"}))
    tags = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Tags", "class": "form-control"}))
    imagem = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}))

    class Meta:
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
            'tags',
            'digital',
            'categoria',
        ]
