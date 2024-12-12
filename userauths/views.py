from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User

#User = settings.AUTH_USER_MODEL

def register_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
           new_user = form.save()
           username = form.cleaned_data.get("username")
           messages.success(request, f"Hey {username}, Sua conta foi criada com sucesso.")
           new_user = authenticate(username=form.cleaned_data['email'],
                                   password=form.cleaned_data['password1']
           )
           login(request, new_user)
           return redirect("core:index")

    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }

    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Ei, você já está logado!")
        return redirect("core:index")


    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Você está logado em sua conta.")
                return redirect("core:index")
            else:
                messages.warning(request, "Usuário não existe. Favor, criar uma conta.")

        except:
            messages.warning(request, f"Usuário {email} não existe.")


    return render(request, "userauths/sign-in.html")



def logout_view(request):
    logout(request)
    messages.success(request, "Voce saiu da sua conta.")
    return redirect("userauths:sign-in")
