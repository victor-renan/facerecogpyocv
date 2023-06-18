from django.urls import path
from . import views as vw


urlpatterns = [
    path('', name="index", view=vw.index_view),
    path('certificate', name="certificate", view=vw.certificate_view),
    path('register', name="register", view=vw.register_view),
    path('login', name="login", view=vw.login_view),
    path('logout', name="logout", view=vw.logout_view)
]