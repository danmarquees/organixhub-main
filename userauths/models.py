from django.db import models
from django.contrib.auth.models import AbstractUser


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

    def __str__(self):
        return self.nome
