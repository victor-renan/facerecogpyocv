from django.shortcuts import render


def index_view(request):
    return render(request, 'base/index.html')


def certificate_view(request):
    return render(request, 'base/certificate.html')