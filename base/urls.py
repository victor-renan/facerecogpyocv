from django.urls import path
from . import views as vw

urlpatterns = [
    path('', name="index", view=vw.index_view),
    path('certificate', name="certificate", view=vw.certificate_view),
]