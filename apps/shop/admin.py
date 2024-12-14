from django.contrib import admin
from .models import Category,Instrument, Supplier, Order, Stock

admin.site.site_header = "Panou de Administrare Site"
admin.site.site_title = "Admin Site"
admin.site.index_title = "Bine ai venit în panoul de administrare"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['instrument','type']
admin.site.register(Category,CategoryAdmin)


class InstrumentAdmin(admin.ModelAdmin):

    list_per_page =  10
    list_display = ['model', 'category', 'price', 'stock']
    list_filter = ['category']  

    # Fieldsets subdivizeaza fieldurile in grupe
    # astfel voi avea informatii de baza care vor avea model si category
    # si detalii produs care vor avea description si price
    fieldsets = [
        ('Informatii de Baza', {
            'fields': ['model', 'category']
        }),
        ('Detalii Produs', {
            'fields': ['description', 'price']
        }),
    ]
  
    # search_fields este un field care permite cautarea dupa un anumit field
    search_fields = ['model']
admin.site.register(Instrument,InstrumentAdmin)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['contact', 'address']
    search_fields = ['address']
admin.site.register(Supplier,SupplierAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'supplier', 'order_date', 'status']
    list_filter = ['status', 'order_date']  
admin.site.register(Order,OrderAdmin)


class StockAdmin(admin.ModelAdmin):
    list_display = ['instrument', 'quantity']
admin.site.register(Stock,StockAdmin)
