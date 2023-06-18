from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
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
            user = mdl.User.objects.create_user(name, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'base/register.html', {
                "error": "Este usuário já existe!"
            })


def login_view(request):
    return render(request, 'base/login.html')