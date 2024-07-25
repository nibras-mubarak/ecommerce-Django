from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
     

class productAdmin(admin.ModelAdmin):
    list_display = ('name',)
     
admin.site.register(category,CategoryAdmin)
admin.site.register(product,productAdmin)