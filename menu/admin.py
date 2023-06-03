from django.contrib import admin
from menu.models import Category, FoodItem



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    # the items will dispaly
    list_display = ('category_name', 'vendor', 'updated_at')
    # to show the search results.
    search_fields = ('category_name', 'vendor__vendor_name')


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('food_title', 'category', 'vendor', 'price', 'is_available', 'updated_at')
    # point the category_name
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name', 'price')
    list_filter = ('is_available',)




admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)