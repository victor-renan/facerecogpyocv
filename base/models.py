from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=300)
    pass


class Certificate(models.Model):
    user = models.ForeignKey('base.User', on_delete=models.CASCADE)
    data = models.DateField(auto_now=True)

    def __str__(self):
        return f"Nome: {self.user.name}, Data: {self.data}"