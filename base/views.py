from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import utils
import re
from . import models as mdl


@login_required(login_url='/login')
def index_view(request):
    existing_certificate = mdl.Certificate.objects.filter(
        user__id=request.user.id)

    context = {"user_certificate": existing_certificate}

    if request.method == "POST":
        desafio1 = request.POST.get("desafio-1")
        desafio2 = request.POST.get("desafio-2")
        desafio = request.POST.get("desafio")
        file_desafio = request.POST.get("file-desafio")

        if desafio1 and desafio2:
            if utils.teste_desafio1(desafio1) and utils.teste_desafio2(desafio2):
                if not existing_certificate:
                    certificate = mdl.Certificate.objects.create(
                        user=mdl.User.objects.get(id=request.user.id),
                    )
                    certificate.save()
                    return HttpResponseRedirect(f'certificates/{certificate.id}')
                else:
                    context = {**context,
                            "error": "Você já emitiu seu certificado!"}
                    return render(request, 'base/index.html', context)
            else:
                if utils.teste_desafio1(desafio1):
                    context = {**context, "sub_success_d1": "Parabéns! Os testes do Desafio 1 foram feitos com êxito!"}
                else:
                    context = {**context, "sub_error_d1": "Ops! O código do Desafio 1 não está como deveria!"}

                if utils.teste_desafio2(desafio2):
                    context = {**context, "sub_success_d2": "Parabéns! Os testes do Desafio 2 foram feitos com êxito!"}
                else:
                    context = {**context, "sub_error_d2": "Ops! O código do Desafio 2 não está como deveria!"}

        if desafio:
            if desafio == "desafio-1":
                if utils.teste_desafio1(file_desafio):
                    context = {
                        **context,
                        "test_success": "Parabéns! Você passou no Desafio 1!",
                        "file_desafio": file_desafio,
                    }
                    return render(request, 'base/index.html', context)
                else:
                    context = {
                        **context,
                        "test_error": "Ops, você não passou no Desafio 1!",
                        "file_desafio": file_desafio
                    }
                    return render(request, 'base/index.html', context)

            elif desafio == "desafio-2":
                if utils.teste_desafio2(file_desafio):
                    context = {
                        **context,
                        "test_success": "Parabéns! Você passou no Desafio 2!",
                        "file_desafio": file_desafio,
                    }
                    return render(request, 'base/index.html', context)
                else:
                    context = {
                        **context,
                        "test_error": "Ops, você não passou no Desafio 2!",
                        "file_desafio": file_desafio
                    }
                    return render(request, 'base/index.html', context)

    return render(request, 'base/index.html', context)


def certificate_view(request):
    return render(request, 'base/certificate.html')


def user_certificate_view(request, id):
    return render(request, 'base/user-certificate.html', {
        "certificate": mdl.Certificate.objects.filter(id=id),
    })


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
        return HttpResponseRedirect(reverse('index'))

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
