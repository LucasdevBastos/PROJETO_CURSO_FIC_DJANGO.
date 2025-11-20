# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Conta criada com sucesso! Você já pode fazer login.")
            return redirect("users:login")
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, "users/register.html", context)
