from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field
from multiselectfield import MultiSelectField
from django.utils import timezone
from django.utils.safestring import mark_safe


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
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

BADGE_CHOICES = (
    ("hot", "Em Destaque"),
    ("new", "Novo"),
    ("sale", "Em Promoção"),
    ("bestseller", "Mais vendido"),
    ("trending", "Tendência"),
    ("recommended", "Recomendado"),
    ("exclusive_deal", "Oferta Exclusiva"),
    ("free_shipping", "Frete Grátis"),
    ("best_price", "Melhor Preço"),
    ("just_arrived", "Recém-Chegado"),
    ("limited_edition", "Edição Limitada"),
    ("organic", "Orgânico"),
    ("handmade", "Feito à Mão"),
    ("locally-made", "Produzido Localmente"),
    ("warranty", "Com Garantia"),
    ("certified", "Certificado"),
    ("five_star-rated", "5 Estrelas"),
    ("last_units", "Últimas Unidades"),
    ("flash_sale", "Oferta Relâmpago"),
    ("today_only", "Por tempo limitado"),
    ("gift_idea", "Sugestão de Presente"),
    ("most_searched", "Mais Procurado"),
    ("combo_deal", "Combo"),
    ("online_only", "Online"),
    ("ready_to_ship", "Envio Imediato"),
    ("pre_order", "Pré-venda"),
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
    capa_imagem = models.ImageField(upload_to=user_directory_path, default="capa.jpg")
    #descricao = models.TextField(null=True, blank=True, default="Sou um vendedor de sucesso")
    descricao = CKEditor5Field(null=True, blank=True, default="Sou um vendedor de sucesso")


    endereco = models.CharField(max_length=100, default="Rua Principal")
    contato = models.CharField(max_length=100, default="+55 (12) 12345 6789")
    tempo_resp_chat = models.CharField(max_length=100, default="100")
    entrega_no_prazo = models.CharField(max_length=100, default="100")
    avaliacao_autenticidade = models.CharField(max_length=100, default="100")
    dias_devolucao = models.CharField(max_length=100, default="100")
    periodo_garantia = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=False, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Vendedores"

    def imagem_vendedor(self):
            return mark_safe('<img src="%s" width="50" height="50" />' % self.imagem.url)

    def __str__(self):
        return self.titulo


class Produto(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=10, alphabet="abcdefgh12345")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='categoria')
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, related_name='produto')


    titulo = models.CharField(max_length=100, default="Lima Laranja", null=True, blank=True)
    imagem = models.ImageField(upload_to=user_directory_path, default="produto.jpg")
    #descricao = models.TextField(null=True, blank=True, default="Este é o produto")
    descricao = CKEditor5Field(null=True, blank=True, default="Este é o produto.")


    preco = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    preco_antigo = models.DecimalField(max_digits=10, decimal_places=2, default=2.99)

    #especificacoes = models.TextField(null=True, blank=True)
    especificacoes = CKEditor5Field(null=True, blank=True)
    tipo = models.CharField(max_length=100, default="Orgânico", null=True, blank=True)
    qtd_estoque = models.IntegerField(default=10, null=True, blank=True) # Changed to IntegerField
    validade = models.CharField(max_length=100, default="100 dias", null=True, blank=True)
    data_fab = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    tags = TaggableManager(blank=True)

    status_produto = models.CharField(choices=STATUS, max_length=10, default="in_review")

    badges = MultiSelectField(choices=BADGE_CHOICES, blank=True, null=True)


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
                if self.preco_antigo and self.preco_antigo > 0:
                    novo_preco = "-" + str(round(((self.preco_antigo - self.preco) / self.preco_antigo) * 100)) + "%"
                    return novo_preco
                return "0%"

    def get_badges(self): #Renamed to avoid conflict
        return self.badges if self.badges else []


class ImagemProduto(models.Model):
    imagens = models.ImageField(upload_to="imagens-produto", default="produto.jpg")
    produto = models.ForeignKey(Produto,related_name="p_imagem", on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Imagens do Produto"

######################################Carrinho, Pedido, Itens e Endereço##################################
######################################Carrinho, Pedido, Itens e Endereço##################################
######################################Carrinho, Pedido, Itens e Endereço##################################
######################################Carrinho, Pedido, Itens e Endereço##################################

class PedidoCarrinho(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=200, null=True, blank=True)
    status_pagamento = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=False, length=4, max_length=10, prefix="sku", alphabet="1234567890")
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status_produto = models.CharField(choices=STATUS_CHOICES, max_length=30, default="processing")
    coupons = models.ManyToManyField('Coupon', blank=True)
    paypal_txn_id = models.CharField(max_length=255, blank=True, null=True)  # Add this field
    payment_date = models.DateTimeField(blank=True, null=True)
    num_fatura = models.CharField(max_length=255, blank=True, null=True) # Novo campo

    class Meta:
        verbose_name_plural = "Pedidos"

    def save(self, *args, **kwargs):
        if not self.num_fatura:
            self.num_fatura = f"INV-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    def get_discount_amount(self):
        from decimal import Decimal
        if not self.coupons.all().exists():
            return Decimal('0.00')
        preco_original = self.get_original_price()
        return Decimal(str(preco_original)) - Decimal(str(self.preco))


    def get_original_price(self):
        from decimal import Decimal
        active_coupons = self.coupons.all().filter(ativo=True)
        if not active_coupons.exists():
            return self.preco

        preco_atual = Decimal(str(self.preco))
        cumulative_discount_factor = Decimal('1.0')

        for coupon in active_coupons:
            discount = Decimal(str(coupon.desconto)) / Decimal('100.0')
            cumulative_discount_factor *= (Decimal('1.0') - discount)

        if cumulative_discount_factor <= 0:
            return Decimal('0.0')

        original_price = preco_atual / cumulative_discount_factor
        return original_price

    def get_final_price(self):
        final_price = self.preco
        for coupon in self.coupons.all():
            final_price -= coupon.get_discount_amount(self.preco)
        return final_price

    def apply_coupon(self, coupon):
        from decimal import Decimal

        if coupon in self.coupons.all():
            raise ValueError("Este cupom já está aplicado ao pedido")

        if not coupon.is_valid():
            raise ValueError("Cupom inválido ou expirado")

        desconto = (Decimal(str(coupon.desconto)) / Decimal('100.0')) * Decimal(str(self.preco))
        novo_preco = self.preco - desconto

        self.coupons.add(coupon)
        self.preco = max(Decimal('0.00'), novo_preco)
        self.save()

        coupon.usos_atuais += 1
        coupon.save()

        return desconto





class ItensPedidoCarrinho(models.Model):
    pedido = models.ForeignKey(PedidoCarrinho, on_delete=models.CASCADE)
    num_fatura = models.CharField(max_length=200)
    status_produto = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    imagem = models.CharField(max_length=200)
    qtd = models.IntegerField(default=0)
    preco = models.DecimalField(max_digits=999999999, decimal_places=2, default=1.99)
    total = models.DecimalField(max_digits=999999999, decimal_places=2, default=1.99)

    class Meta:
         verbose_name_plural = "Itens de Pedidos"

    def imagem_produto(self):
            return mark_safe('<img src= "%s" width="50" height="50" />' % (self.imagem.url))

    def imagem_pedido(self):
            return mark_safe('<img src= "/media/%s" width="50" height="50" />' % (self.imagem))

######################################Avaliação do Produto, Lista de Desejos, Endereço##################################
######################################Avaliação do Produto, Lista de Desejos, Endereço##################################
######################################Avaliação do Produto, Lista de Desejos, Endereço##################################
######################################Avaliação do Produto, Lista de Desejos, Endereço##################################

class AvaliacaoProduto(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, related_name="reviews")
    avaliacao = models.TextField()
    classificacao = models.IntegerField(choices=RATING, default=None)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
            verbose_name_plural = "Avaliações do Produto"

    def imagem_produto(self):
            return mark_safe('<img src= "%s" width="50" height="50" />' % (self.imagem.url))

    def __str__(self):
            return str(self.produto.titulo) if self.produto else "Produto não especificado"


    def obter_classificacao(self):
        return self.classificacao


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
            verbose_name_plural = "Wishlists"

    def __str__(self):
        return str(self.produto.titulo)


class Endereco(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cep = models.CharField(max_length=9, null=True)
    logradouro = models.CharField(max_length=255, null=True)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True)
    localidade = models.CharField(max_length=255, null=True)
    uf = models.CharField(max_length=2, null=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True) # Added cellphone field
    status = models.BooleanField(default=False)


    class Meta:
            verbose_name_plural = "Endereço"


class Coupon(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_validade = models.DateTimeField(null=True, blank=True)
    valor_minimo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usos_maximos = models.IntegerField(null=True, blank=True)
    usos_atuais = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Cupom'
        verbose_name_plural = 'Cupons'

    def __str__(self):
        return f"{self.codigo} ({self.desconto}% off)"

    def is_valid(self):
        """Verifica se o cupom é válido"""
        # Verifica se o cupom está ativo
        if not self.ativo:
            return False

        # Verifica a data de validade
        if self.data_validade and timezone.now() > self.data_validade:
            return False

        # Verifica o número máximo de usos
        if self.usos_maximos and self.usos_atuais >= self.usos_maximos:
            return False

        return True

    def check_validity(self):
        """Verifica a validade e retorna mensagem de erro se houver"""
        if not self.ativo:
            raise ValueError("Este cupom não está mais ativo")

        if self.data_validade and timezone.now() > self.data_validade:
            raise ValueError("Este cupom está expirado")

        if self.usos_maximos and self.usos_atuais >= self.usos_maximos:
            raise ValueError("Este cupom atingiu o limite máximo de usos")

        return True
