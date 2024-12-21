from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


"""
    Dupa ce creezi un user/superuser in admin
    care se creeaza doar prin introducerea unui
    username, email si parola poti sa te duci
    in pagina de admin si dupa ce dai click
    pe userul pe care doresti sa il editezi
    poti sa completezi/editezo toate campurile
    adaugandu-le in fieldsets si multe altele
"""

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'telefon', 'adresa'] 
    fieldsets = UserAdmin.fieldsets + (
        ('Informații adiționale', {'fields': ('telefon', 'adresa')}),  
    )


admin.site.register(CustomUser, CustomUserAdmin)