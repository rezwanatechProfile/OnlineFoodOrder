from django.contrib import admin
from django.contrib import admin
from .models import Payment, Order, OrderedFood



class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    # make the items readable for the admin
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'phone', 'email', 'total', 'payment_method', 'status', 'is_ordered']
    inlines = [OrderedFoodInline]

# Register your models here.
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)