from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Adăugăm câmpurile personalizate în admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informații adiționale', {'fields': ('phone', 'address')}),  # înlocuiți cu câmpurile voastre
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informații adiționale', {'fields': ('phone', 'address')}),  # înlocuiți cu câmpurile voastre
    )

admin.site.register(CustomUser, CustomUserAdmin)