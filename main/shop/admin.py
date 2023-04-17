from django.contrib import admin
from .models import *

admin.site.register(UserCustom)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)



