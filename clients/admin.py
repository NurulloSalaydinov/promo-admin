from django.contrib import admin
from .models import Visitor, Client, Order


admin.site.register(Visitor)
admin.site.register(Client)
admin.site.register(Order)

