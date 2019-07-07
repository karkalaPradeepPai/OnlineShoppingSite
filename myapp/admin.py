
from django.contrib import admin
from .models import Product, Category, Client, Order

# Register your models here.
#admin.site.register(Product)
#admin.site.register(Category)
#admin.site.register(Client)
#admin.site.register(Order)
class CategoryAdmin(admin.ModelAdmin):

    fields= ['name','warehouse']

    list_filter =['name','warehouse']

    list_display =['name','warehouse']

    list_editable =['warehouse']

    search_fields = ['warehouse']


def refill(modeladmin, request, queryset):
    for q in queryset:
        old_stock = q.stock
        new_stock = old_stock+50
        queryset.update(stock=new_stock)
    refill.short_description = "Increment Stock by 50"

class ProductAdmin(admin.ModelAdmin):

   fields = ('name', 'category', 'price', 'available','stock')
   actions = [refill]

   list_filter =['name','category','price','available','stock','description','interested']

   list_display =['name','category','price','available','stock','description','interested']

   list_editable =['price']

   search_fields = ['category__name']

class ClientAdmin(admin.ModelAdmin):

    fields= ['company','city','province','interested_in','shipping_address']

    list_filter =['company','city','province','interested_in','shipping_address']

    search_fields = ['city']

    list_display = ['city','company','province','shipping_address']

    list_editable =['shipping_address']




class OrderAdmin(admin.ModelAdmin):

    fields= ['client','product','num_units','status_date','order_status']

    search_fields = ['product__name']

    list_filter =['client','product','num_units','status_date','order_status']

    list_display =['client','product','num_units','status_date','order_status']

    list_editable =['product']


admin.site.register(Client,ClientAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)