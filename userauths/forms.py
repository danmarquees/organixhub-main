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
