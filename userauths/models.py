from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    primeiro_nome = models.CharField(max_length=255, blank=True)
    ultimo_nome = models.CharField(max_length=255, blank=True)



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to="image")
    nome = models.CharField(max_length=255, null=True,blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    telefone = models.CharField(max_length=200)
    verificado = models.BooleanField(default=False)

    # Campos de endereço adicionados
    rua = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    cep = models.CharField(max_length=9, null=True, blank=True)


    def __str__(self):
            if self.nome:
                return self.nome
            else:
                return "Profile (no name set)"



class Contato(models.Model):
    nome = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)
    assunto = models.CharField(max_length=200)
    mensagem = models.TextField()

    def __str__(self):
        return self.nome


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

class Vendedor(models.Model):
    # Informações Pessoais ou Empresariais
    nome_completo = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    rg = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField()

    # Informações de Contato
    email = models.EmailField(unique=True)
    telefone_celular = models.CharField(max_length=15)
    telefone_comercial = models.CharField(max_length=15, blank=True, null=True)

    # Endereço detalhado
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=9)

    # Informações sobre a Loja
    nome_loja = models.CharField(max_length=100)
    categoria_produtos = models.CharField(max_length=50)
    descricao_loja = models.TextField(blank=True, null=True)
    logotipo = models.ImageField(upload_to="vendedores/logotipos/", blank=True, null=True)

    # Informações Bancárias
    nome_banco = models.CharField(max_length=50)
    numero_conta = models.CharField(max_length=20)
    agencia = models.CharField(max_length=10)
    tipo_conta = models.CharField(
        max_length=10,
        choices=[('corrente', 'Conta Corrente'), ('poupanca', 'Conta Poupança')]
    )
    titular_conta = models.CharField(max_length=100)

    # Termos e Condições
    aceite_termos = models.BooleanField(default=False)

    def __str__(self):
        return self.nome_loja
