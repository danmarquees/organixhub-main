from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field
from multiselectfield import MultiSelectField
from django.utils import timezone
from django.utils.safestring import mark_safe
import uuid


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
    reputacao = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)



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
    preco_antigo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)


    #especificacoes = models.TextField(null=True, blank=True)
    especificacoes = CKEditor5Field(null=True, blank=True)
    tipo = models.CharField(max_length=100, default="Orgânico", null=True, blank=True)

    qtd_estoque = models.IntegerField(default=10, null=True, blank=True) # Changed to IntegerField
    qtd_vendida = models.IntegerField(default=0, null=True, blank=True)  # Contador de vendas

    validade = models.CharField(max_length=100, default="100 dias", null=True, blank=True)
    data_fab = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    meta_titulo = models.CharField(max_length=150, null=True, blank=True)
    meta_descricao = models.TextField(null=True, blank=True)
    palavras_chave = models.CharField(max_length=255, null=True, blank=True)

    inicio_promocao = models.DateTimeField(null=True, blank=True)  # Início da oferta
    fim_promocao = models.DateTimeField(null=True, blank=True)  # Fim da oferta

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
        verbose_name_plural = "Lista de Produtos"

    def imagem_produto(self):
            return mark_safe('<img src= "%s" width="50" height="50" />' % (self.imagem.url))

    def __str__(self):
        return self.titulo

    def em_promocao(self):
            """Verifica se o produto está em promoção no momento."""
            if self.inicio_promocao and self.fim_promocao:
                agora = timezone.now()
                return self.inicio_promocao <= agora <= self.fim_promocao
            return False

    def tempo_restante_promocao(self):
        """Retorna o tempo restante para o fim da promoção."""
        if self.em_promocao():
            return self.fim_promocao - timezone.now()
        return None

    def obter_porcentagem(self):
                    if self.preco_antigo and self.preco_antigo > 0:
                        novo_preco = str(round(((self.preco_antigo - self.preco) / self.preco_antigo) * 100)) + "%"
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

class VariacaoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="variacoes")
    nome = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)


######################################Carrinho, Pedido, Itens e Endereço##################################
######################################Carrinho, Pedido, Itens e Endereço##################################
######################################Carrinho, Pedido, Itens e Endereço##################################
######################################Carrinho, Pedido, Itens e Endereço##################################

class PedidoCarrinho(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Chave estrangeira para o modelo User, definindo o usuário que fez o pedido. Se o usuário for excluído, o pedido também será excluído.

    nome = models.CharField(max_length=200, null=True, blank=True) # Nome do cliente, permite valores nulos e em branco.
    email = models.EmailField(max_length=200, null=True, blank=True) # Email do cliente, permite valores nulos e em branco.
    endereco = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True) # Número de telefone do cliente, permite valores nulos e em branco.
    cidade = models.CharField(max_length=200, null=True, blank=True) # Cidade do cliente, permite valores nulos e em branco.
    estado = models.CharField(max_length=200, null=True, blank=True) # Estado do cliente, permite valores nulos e em branco.
    cep = models.CharField(max_length=9, null=True, blank=True)

    status_pagamento = models.BooleanField(default=False) # Campo booleano indicando se o pagamento foi feito, padrão False.
    sku = ShortUUIDField(unique=False, length=4, max_length=10, prefix="SKU", alphabet="1234567890") # Campo ShortUUID para SKU, não único.
    orderid = ShortUUIDField(unique=False, length=4, max_length=10, alphabet="1234567890") # Campo ShortUUID para ID do pedido, não único.

    preco = models.DecimalField(max_digits=10, decimal_places=2, default=1.99) # Preço total do pedido, padrão 1.99.
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=1.99) # Desconto aplicado ao pedido, padrão 1.99.
    data_pedido = models.DateTimeField(auto_now_add=True) # Registra automaticamente a data e hora do pedido.

    status_produto = models.CharField(choices=STATUS_CHOICES, max_length=30, default="processing") # Status do pedido, as opções são definidas em STATUS_CHOICES.
    coupons = models.ManyToManyField('Coupon', blank=True, related_name="pedidos") # Relacionamento muitos-para-muitos com o modelo Coupon, permitindo múltiplos cupons por pedido.
    num_fatura = models.CharField(max_length=255, blank=True, null=True) # Número da fatura, permite valores nulos e em branco.

    payment_date = models.DateTimeField(null=True, blank=True) # Data e hora do pagamento, permite valores nulos e em branco.
    metodo_entrega = models.CharField(max_length=100, choices=[('delivery', 'Entrega'), ('pickup', 'Retirada')], default='delivery') # Método de entrega, as opções são 'delivery' ou 'pickup'.
    id_rastreamento = models.CharField(max_length=255, blank=True, null=True) # ID de rastreamento, permite valores nulos e em branco.
    impostos = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Valor dos impostos, padrão 0.00.
    taxas = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Valor das taxas, padrão 0.00.


    class Meta:
        verbose_name_plural = "Pedidos"

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para gerar um número de fatura único se ele não existir.
        """
        if not self.num_fatura:
            # Gera um número de fatura com o formato INV-AAAAAMMDDHHMMSS
            self.num_fatura = f"INV-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        # Chama o método save da classe pai
        super().save(*args, **kwargs)

    def get_discount_amount(self):
        """
        Calcula o valor total do desconto aplicado aos cupons.
        """
        from decimal import Decimal
        # Se não houver cupons aplicados, retorna 0.00
        if not self.coupons.exists():
            return Decimal('0.00')
        # Obtém o preço original do pedido antes dos descontos
        preco_original = self.get_original_price()
        # Calcula e retorna o valor total do desconto
        return preco_original - self.preco


    def get_original_price(self):
        """
        Calcula o preço original do pedido antes dos descontos.
        """
        from decimal import Decimal
        # Obtém os cupons ativos aplicados ao pedido
        active_coupons = self.coupons.filter(ativo=True)
        # Se não houver cupons ativos, retorna o preço atual
        if not active_coupons.exists():
            return self.preco

        # Converte o preço atual para Decimal
        preco_atual = Decimal(str(self.preco))
        # Inicializa o fator de desconto acumulado com 1.0
        cumulative_discount_factor = Decimal('1.0')

        # Itera sobre os cupons ativos
        for coupon in active_coupons:
            # Calcula o desconto percentual de cada cupom
            discount = Decimal(str(coupon.desconto)) / Decimal('100.0')
            # Atualiza o fator de desconto acumulado
            cumulative_discount_factor *= (Decimal('1.0') - discount)

        # Se o fator de desconto acumulado for menor ou igual a 0, retorna 0.0
        if cumulative_discount_factor <= 0:
            return Decimal('0.0')

        # Calcula e retorna o preço original
        original_price = preco_atual / cumulative_discount_factor
        return original_price

    def get_final_price(self):
        """
        Calcula o preço final do pedido após aplicar os descontos.
        """
        from decimal import Decimal
        final_price = self.preco

        return final_price

    def apply_coupon(self, coupon):
        """
        Aplica um cupom ao pedido.
        """
        from decimal import Decimal

        # Verifica se o cupom já foi aplicado
        if coupon in self.coupons.all():
            raise ValueError("Este cupom já está aplicado ao pedido")

        # Verifica a validade do cupom
        if not coupon.is_valid():
            raise ValueError("Cupom inválido ou expirado")

        if self.preco is None:
            raise ValueError("O preço do pedido não pode ser None.")

        # Calcula o valor do desconto
        desconto_decimal = Decimal(str(coupon.desconto)) / Decimal('100.0')
        desconto = desconto_decimal * self.preco

        # Calcula o novo preço após aplicar o desconto
        novo_preco = self.preco - desconto

        # Adiciona o cupom ao pedido
        self.coupons.add(coupon)
        # Atualiza o preço do pedido
        self.preco = max(Decimal('0.00'), novo_preco)
        # Salva as alterações no pedido
        self.save()

        # Atualiza o número de usos do cupom
        coupon.usos_atuais += 1
        coupon.save()

        # Retorna o valor do desconto
        return desconto





class ItensPedidoCarrinho(models.Model):
    pedido = models.ForeignKey(PedidoCarrinho, on_delete=models.CASCADE)
    orderid = ShortUUIDField(unique=False, length=4, max_length=10, alphabet="1234567890")
    num_fatura = models.CharField(max_length=255, blank=True, null=True)
    status_produto = models.CharField(max_length=200)
    item = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, related_name="itens_pedido")
    imagem = models.CharField(max_length=200, blank=True, null=True) # Added blank=True, null=True
    qtd = models.IntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=1.99) # Reduced max_digits
    total = models.DecimalField(max_digits=10, decimal_places=2, default=1.99) # Reduced max_digits

    class Meta:
         verbose_name_plural = "Itens de Pedidos"

    def imagem_produto(self):
            return mark_safe('<img src= "%s" width="50" height="50" />' % (self.imagem.url))

    def imagem_pedido(self):
            return mark_safe('<img src= "/media/%s" width="50" height="50" />' % (self.imagem))

    def save(self, *args, **kwargs):
            """Atualiza o contador de vendas ao salvar um item no pedido."""
            super().save(*args, **kwargs)
            if self.item:
                self.item.qtd_vendida += self.qtd
                self.item.save()


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
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

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
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)


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


class Chat(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensagens_enviadas")
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensagens_recebidas")
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_envio = models.DateTimeField(auto_now_add=True)


class HistoricoAtividade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acao = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)


class RelatorioVendas(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    total_vendas = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class MetodoPagamento(models.Model):
    nome = models.CharField(max_length=100)
    taxa = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ativo = models.BooleanField(default=True)
