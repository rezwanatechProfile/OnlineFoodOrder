from .models import Cart
from menu.models import FoodItem
from rest_framework import serializers

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


# class CartCounterSerializer(serializers.Serializer):
#     cart_count = serializers.IntegerField()

# def get_cart_counter(request):
#     cart_count = 0
#     if request.user.is_authenticated:
#         try:
#             cart_items = Cart.objects.filter(user=request.user)
#             if cart_items:
#                 for cart_item in cart_items:
#                     cart_count += cart_item.quantity
#             else:
#                 cart_count = 0
#         except:
#             cart_count = 0
#     serializer = CartCounterSerializer({'cart_count': cart_count})
#     return serializer.data

# to get the access of subtotal, tax and granttotal in all html pages
def get_cart_amounts(request):
    subtotal = 0
    tax = 0
    grand_total = 0
    # tax_dict = {}
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += (fooditem.price * item.quantity) # subtotal = subtotal + (fooditem.price * item.quantity)

        grand_total = subtotal + tax

    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total)