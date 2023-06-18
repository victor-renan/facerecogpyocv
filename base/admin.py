from django.contrib import admin
from . import models as mdl


admin.site.register(mdl.User)
admin.site.register(mdl.Certificate)
