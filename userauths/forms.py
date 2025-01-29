from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Nome de Usuário"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Senha"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirmar Senha"}))

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Nome de Usuário"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Telefone"}))
    class Meta:
        model = Profile
        fields = ['nome', 'imagem', 'bio', 'telefone']


from django import forms

class VendedorForm(forms.Form):
    # Informações Pessoais ou Empresariais
    nome_completo = forms.CharField(label='Nome Completo', max_length=100)
    cpf_cnpj = forms.CharField(label='CPF ou CNPJ', max_length=18)
    rg = forms.CharField(label='RG (opcional)', max_length=15, required=False)
    data_nascimento = forms.DateField(label='Data de Nascimento', widget=forms.DateInput(attrs={'type': 'date'}))

    # Informações de Contato
    email = forms.EmailField(label='E-mail')
    telefone_celular = forms.CharField(label='Telefone Celular', max_length=15)
    telefone_comercial = forms.CharField(label='Telefone Comercial', max_length=15, required=False)

    # Endereço detalhado
    rua = forms.CharField(label='Rua', max_length=100)
    numero = forms.CharField(label='Número', max_length=10)
    bairro = forms.CharField(label='Bairro', max_length=100)
    cidade = forms.CharField(label='Cidade', max_length=100)
    estado = forms.CharField(label='Estado', max_length=50)
    cep = forms.CharField(label='CEP', max_length=9)

    # Informações sobre a Loja
    nome_loja = forms.CharField(label='Nome da Loja', max_length=100)
    categoria_produtos = forms.CharField(label='Categoria de Produtos', max_length=50)
    descricao_loja = forms.CharField(
        label='Descrição da Loja',
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )
    logotipo = forms.ImageField(label='Logotipo ou Foto Representativa', required=False)

    # Informações Bancárias
    nome_banco = forms.CharField(label='Nome do Banco', max_length=50)
    numero_conta = forms.CharField(label='Número da Conta', max_length=20)
    agencia = forms.CharField(label='Agência', max_length=10)
    tipo_conta = forms.ChoiceField(
        label='Tipo de Conta',
        choices=[('corrente', 'Conta Corrente'), ('poupanca', 'Conta Poupança')]
    )
    titular_conta = forms.CharField(label='Nome do Titular da Conta', max_length=100)

    # Termos e Condições
    aceite_termos = forms.BooleanField(label='Aceito os Termos de Uso e Política de Privacidade')
