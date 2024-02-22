from django.contrib import admin

# Register your models here.
from .models import UserDiet, DetailOfDiet

admin.site.register(UserDiet)
admin.site.register(DetailOfDiet)
