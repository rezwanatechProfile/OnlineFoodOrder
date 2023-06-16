
from django.shortcuts import render, redirect
from urllib import response
from django.http import HttpResponse, JsonResponse
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
from menu.models import FoodItem
from .forms import OrderForm
from .models import Order, OrderedFood, Payment
import simplejson as json
from .utils import generate_order_number
# from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

# @login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')

    vendors_ids = []
    for i in cart_items:
        if i.fooditem.vendor.id not in vendors_ids:
            vendors_ids.append(i.fooditem.vendor.id)
    
    # # {"vendor_id":{"subtotal":{"tax_type": {"tax_percentage": "tax_amount"}}}}
    # get_tax = Tax.objects.filter(is_active=True)
    subtotal = 0
    total_data = {}
    k = {}
    for i in cart_items:
        fooditem = FoodItem.objects.get(pk=i.fooditem.id, vendor_id__in=vendors_ids)
        v_id = fooditem.vendor.id
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (fooditem.price * i.quantity)
            k[v_id] = subtotal
        else:
            subtotal = (fooditem.price * i.quantity)
            k[v_id] = subtotal
    
        # Construct total data
        total_data.update({fooditem.vendor.id: {str(subtotal)}})

            # Construct total data
        if fooditem.vendor.id in total_data:
            total_data[fooditem.vendor.id].add(str(subtotal))
        else:
            total_data[fooditem.vendor.id] = {str(subtotal)}

# Serialize total_data
    serialized_total_data = {}
    for key, value in total_data.items():
        serialized_total_data[str(key)] = list(value)

    total_data = json.dumps(serialized_total_data)

    print("hello", total_data)
    

        

    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    # tax_data = get_cart_amounts(request)['tax_dict']
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.zip_code = form.cleaned_data['zip_code']
            # need the userid 
            order.user = request.user

            order.total = grand_total
            # order.tax_data = json.dumps(tax_data)
            order.total_data = total_data
            order.total_tax = total_tax
            #  the below field is coming from here<input type="radio" name="payment_method" value="PayPal">
            order.payment_method = request.POST['payment_method']
            order.save() # order id/ pk is generated
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendors_ids)
            order.save()

            context = {
                'order': order,
                'cart_items': cart_items,
            }
            return render(request, 'orders/place_order.html', context)

        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')



@login_required(login_url='login')
def payments(request):
    # Check if the request is ajax or not
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
          
    # STORE THE PAYMENT DETAILS IN THE PAYMENT MODEL (get the transaction id and details)
          order_number = request.POST.get('order_number')
          transaction_id = request.POST.get('transaction_id')
          payment_method = request.POST.get('payment_method')
          status = request.POST.get('status')

          print(order_number, transaction_id, payment_method, status)

          order = Order.objects.get(user=request.user, order_number=order_number)
          payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
          )
          payment.save()

        # UPDATE THE ORDER MODEL
          order.payment = payment
          order.is_ordered = True
          order.save()

        # MOVE THE CART ITEMS TO ORDERED FOOD MODEL
          cart_items = Cart.objects.filter(user=request.user)
          for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity # total amount
            ordered_food.save()
             # CLEAR THE CART IF THE PAYMENT IS SUCCESS
            cart_items.delete() 

   

    #     # RETURN BACK TO AJAX WITH THE STATUS SUCCESS OR FAILURE
          response = {
            'order_number': order_number,
            'transaction_id': transaction_id,
        }
          return JsonResponse(response)
    return HttpResponse('Payments view')


def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')

    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)

        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)

        # tax_data = json.loads(order.tax_data)
        # print(tax_data)
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
        }

        return render(request, 'orders/order_complete.html', context)
    except:
        return redirect('home')