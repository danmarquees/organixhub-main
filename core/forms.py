from django import forms
from core.models import AvaliacaoProduto

class AvaliacaoProdutoForm(forms.ModelForm):
    avaliacao = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Deixe uma avaliação"}))

    class Meta:
        model = AvaliacaoProduto
        fields =['avaliacao', 'classificacao']
