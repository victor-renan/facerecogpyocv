from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import models as mdl


@login_required(login_url='/login')
def index_view(request):
    return render(request, 'base/index.html')


def certificate_view(request):
    return render(request, 'base/certificate.html')


def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if password != confirmation:
            return render(request, 'base/register.html', {
                "error": "As senhas não conferem!"
            })
        try:
            user = mdl.User.objects.create_user(
                name=name,
                username=email,
                password=password)
            
            user.save()
        except IntegrityError:
            return render(request, 'base/register.html', {
                "error": "Este usuário já existe!"
            })
        
        login(request, user)
        HttpResponseRedirect(reverse('index'))

        
    return render(request, 'base/register.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user != None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'base/login.html', {
                "error": "Email ou senha inválidos!"
            })
    else:
        return render(request, 'base/login.html')
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))