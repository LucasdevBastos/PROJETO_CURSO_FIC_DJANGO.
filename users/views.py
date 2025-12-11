# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Faz login automático após cadastro
            login(request, user)
            messages.success(request, "Conta criada com sucesso! Bem-vindo(a)!")
            return redirect("anime:anime_list")  # Redireciona direto para lista de animes
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, "users/register.html", context)
