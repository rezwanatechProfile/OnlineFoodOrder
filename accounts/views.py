import json
from django.http import JsonResponse
from django.shortcuts import redirect, render

from orders.models import Order

# from .serailizers import UserSerializer
from .utils import detectUser
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User
from .signals import UserProfile
from django.contrib import messages, auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from vendor.models import Vendor
from django.template.defaultfilters import slugify
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
# from rest_framework import status, views
# from rest_framework.authtoken.models import Token
# from vendor.serializers import UserProfileSerializer


#Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied



#Restrict the customer from accessing the vendor page

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

   

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('custDashboard')
    elif request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # form.cleaned_data is a dictionary-like object that contains the cleaned/formatted data submitted through an HTML form. It is typically accessed after validating a form using the is_valid() method.
            # When a form is submitted, Django performs various cleaning and validation operations on the submitted data. This includes converting the input into the appropriate Python data types, applying any field-specific validation rules, and handling any custom cleaning methods defined in the form.
            # password = form.cleaned_data['password']
            # commit=False (assign the role to the user) means the form is ready to be saved. whatever data 
            # we have in the form it will assign to the user
            # user = form.save(commit=False)
            # user.set_password(password)
            # create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER 
            user.save()
             # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            # send_verification_email(request, user)

            messages.success(request, 'Your account has been registered successfully')
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form=UserForm()
    # "context" refers to a dictionary-like object that contains data and variables that are accessible within a Django template.
    context = {
        'form': form,
      }
    return render(request, 'accounts/registerUser.html', context)


# REGISTER VENDOR FUNCTION
def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('vendorDashboard')  

    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            print(user)

            vendor = v_form.save(commit=False)
            vendor.user = user
            # when any restaurant owner   register vendor_slug will be automatically generated
            vendor_name = v_form.cleaned_data['vendor_name']
            # concatinate user id so any vendor can not register with the same name. with user id it is going to be unique. 
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            try:
                userprofile = UserProfile.objects.get(user=user)
                vendor.userprofile = userprofile
                vendor.save()
            except:
                UserProfile.DoesNotExist
                print("no matching userprofile")


            # Send verification email
            # mail_subject = 'Please activate your account'
            # email_template = 'accounts/emails/account_verification_email.html'
            # send_verification_email(request, user)

            messages.success(request, 'Your account has been registered sucessfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)

# TO ACTIVATE THE USER FROM THE EMAIL
# def activate(request, uidb64, token):
#     # Activate the user by seeting the is_active status to true
#     try:
#         # urlsafe_base64_decode to decode the value from utils 
#         uid = urlsafe_base64_decode(uidb64)
#         user = User._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Congratulation! Your account is activated.')
#         return redirect('myAccount')
#     else:
#         messages.error(request, 'Invalid activation link')
#         return redirect('myAccount')


# login path
def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # authenticating the user
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid loging credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

# @api_view(['POST'])
# def login(request):
#     # if request.user.is_authenticated:
#     #     return JsonResponse({'message': 'You are already logged in'})

#     if request.method == 'POST':
#         email = request.data.get('email')
#         if email is None:
#             error_message = 'Email field is missing'
#             return JsonResponse({'status': 'Failed', 'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
#         password = request.data.get('password')
#         if password is None:
#             error_message = 'Password field is missing'
#             return JsonResponse({'status': 'Failed', 'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
#         # authenticating the user
#         user = auth.authenticate(request, email=email, password=password)
        
#         if user is not None:
#             auth.login(request, user)
#             # Generate or get the token for the user
#             token, created = Token.objects.get_or_create(user=user)
#             return JsonResponse({
#                 'message': 'You are now logged in',
#                 'token': token.key
#             })
#         else:
#             return JsonResponse({'status': 'Failed', 'message': 'Invalid login credentials'}, status=400)

#     return JsonResponse({'status': 'Failed', 'message': 'Invalid request method'}, status=400)


# Profile View

# class ProfileView(views.APIView):
#     authentication_classes=[TokenAuthentication, ]
#     permission_classes = [IsAuthenticated, ]
    
#     def get(self,request):
#         try:
#             query = UserProfile.objects.get(user=request.user)
#             serializer = UserProfileSerializer(query)
#             response_message = {"error":False,"data":serializer.data}
#         except:
#             response_message = {"error":True,"message":"Somthing is Wrong"}
#         return Response(response_message)


# class UserUpdate(views.APIView):
#     permission_classes=[IsAuthenticated, ]
#     authentication_classes=[TokenAuthentication, ]
#     def post(self,request):
#         try:
#             user = request.user
#             query = UserProfile.objects.get(user=user)
#             data = request.data
#             serializers = UserProfileSerializer(query,data=data,context={"request":request})
#             serializers.is_valid(raise_exception=True)
#             serializers.save()
#             return_res={"message":"Profile is Updated"}
#         except:
#             return_res={"message":"Somthing is Wrong Try Agane !"}
#         return Response(return_res)


# logout path
def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out")
    return redirect('login')


# myAccount should run only when the user is logged in. for that we need to use login decorator. 
# If the user is not logged in it will send the user to the log in page.
@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)
# go to the utils.py to create helper function


# custDashboard should run only when the user is logged in. for that we need to use login decorator. 
# If the user is not logged in it will send the user to the log in page.
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    # to send the order information into the customer order page
    orders = Order.objects.filter(user=request.user, is_ordered=True)[:5]
    context = {
        'orders': orders,
        'orders_count': orders.count()

    }
    return render(request, 'accounts/custDashboard.html', context)


# vendorDashboard should run only when the user is logged in. for that we need to use login decorator. 
# If the user is not logged in it will send the user to the log in page.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('created_at')
    print(orders)
    recent_orders = orders[:5]
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders
      
    }
    return render(request, 'accounts/vendorDashboard.html', context)


