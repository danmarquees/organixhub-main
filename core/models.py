from email.policy import default
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User

STATUS_CHOICES = (
    ("processing", "Em Processamento"),
    ("shipped", "Enviado"),
    ("delivered", "Entregue"),
)

STATUS = (
    ("draft", "Rascunho"),
    ("disabled", "Desativado"),
    ("rejected", "Rejeitado"),
    ("in_review", "Em Revisão"),
    ("published", "Publicado"),
)

RATING = (
    ("1", "★☆☆☆☆"),
    ("2", "★★☆☆☆"),
    ("3", "★★★☆☆"),
    ("4", "★★★★☆"),
    ("5", "★★★★★"),
)

def user_directory_path(instance, filename):
    return 'usuario_{0}/{1}'.format(instance.user.id, filename)

class Categoria(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=10, prefix="cat", alphabet="abcdefgh12345")
    titulo = models.CharField(max_length=100, default="Alimentos")
    imagem = models.ImageField(upload_to="categoria", default="categoria.jpg")

    class Meta:
        verbose_name_plural = "Categorias"

    def imagem_categoria(self):
        if self.imagem:
            return mark_safe('<img src= "%s" width="50" height="50" />' % (self.imagem.url))
        return ''

    def __str__(self):
        return self.titulo

class Tags(models.Model):
    pass

class Vendedor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=10, prefix="ven", alphabet="abcdefgh12345")

    titulo = models.CharField(max_length=100, default="Organyx")
    imagem = models.ImageField(upload_to=user_directory_path, default="vendedor.jpg")
    descricao = models.TextField(null=True, blank=True, default="Sou um vendedor de sucesso")

    endereco = models.CharField(max_length=100, default="Rua Principal")
    contato = models.CharField(max_length=100, default="+55 (12) 12345 6789")
    tempo_resp_chat = models.CharField(max_length=100, default="100")
    entrega_no_prazo = models.CharField(max_length=100, default="100")
    avaliacao_autenticidade = models.CharField(max_length=100, default="100")
    dias_devolucao = models.CharField(max_length=100, default="100")
    periodo_garantia = models.CharField(max_length=100, default="100")

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Vendedores"

    def imagem_vendedor(self):
            return mark_safe('<img src="%s" width="50" height="50" />' % self.imagem.url)

    def __str__(self):
        return self.titulo

class Produto(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=10, alphabet="abcdefgh12345")

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    titulo = models.CharField(max_length=100, default="Lima Laranja")
    imagem = models.ImageField(upload_to=user_directory_path, default="produto.jpg")
    descricao = models.TextField(null=True, blank=True, default="Este é o produto")

    preco = models.DecimalField(max_digits=999999999, decimal_places=2, default=1.99)
    preco_antigo = models.DecimalField(max_digits=999999999, decimal_places=2, default=2.99)

    especificacoes = models.TextField(null=True, blank=True)
    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    status_produto = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    em_estoque = models.BooleanField(default=False)
    destaque = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")

    data = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Produtos"

    def imagem_produto(self):
            return mark_safe('<img src= "%s" width="50" height="50" />' % (self.imagem.url))

    def __str__(self):
        return self.titulo

    def obter_porcentagem(self):
        novo_preco = float(str(self.preco)) / float(str(self.preco_antigo)) * 100
        return novo_preco

class ImagemProduto(models.Model):
    imagens = models.ImageField(upload_to="imagens-produto", default="produto.jpg")
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Imagens do Produto"

######################################Carrinho, Pedido, Itens e Endereço##################################
######################################Carrinho, Pedido, Itens e Endereço##################################
######################################Carrinho, Pedido, Itens e Endereço##################################
######################################Carrinho, Pedido, Itens e Endereço##################################

class PedidoCarrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=999999999, decimal_places=2, default=1.99)
    status_pagamento = models.BooleanField(default=False)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status_produto = models.CharField(choices=STATUS_CHOICES, max_length=30, default="processing")

    class Meta:
         verbose_name_plural = "Pedidos do Carrinho"

class ItensPedidoCarrinho(models.Model):
    pedido = models.ForeignKey(User, on_delete=models.CASCADE)
    num_fatura = models.CharField(max_length=200)
    status_produto = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    imagem = models.CharField(max_length=200)
    qtd = models.IntegerField(default=0)
    preco = models.DecimalField(max_digits=999999999, decimal_places=2, default=1.99)
    total = models.DecimalField(max_digits=999999999, decimal_places=2, default=1.99)

    class Meta:
         verbose_name_plural = "Itens do Pedido do Carrinho"

    def imagem_pedido(self):
            return mark_safe('<img src= "/media/%s" width="50" height="50" />' % (self.imagem))

######################################Avaliação do Produto, Lista de Desejos, Endereço##################################
######################################Avaliação do Produto, Lista de Desejos, Endereço##################################
######################################Avaliação do Produto, Lista de Desejos, Endereço##################################
######################################Avaliação do Produto, Lista de Desejos, Endereço##################################

class AvaliacaoProduto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    avaliacao = models.TextField()
    classificacao = models.IntegerField(choices=RATING, default=None)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
            verbose_name_plural = "Avaliações do Produto"

    def imagem_produto(self):
            return mark_safe('<img src= "%s" width="50" height="50" />' % (self.imagem.url))

    def __str__(self):
        return str(self.produto.titulo)


    def obter_classificacao(self):
        return self.classificacao


class Wishlist(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
            verbose_name_plural = "Wishlists"

    def __str__(self):
        return str(self.produto.titulo)


class Endereco(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    endereco = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
            verbose_name_plural = "Endereço"
