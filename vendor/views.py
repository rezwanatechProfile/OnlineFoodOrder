from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import UserProfile
from menu.forms import CategoryForm
from vendor.models import Vendor

from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from django.template.defaultfilters import slugify




# get_vendor function to use it in all functions. To not repeat
def get_vendor(request):
     vendor = Vendor.objects.get(user=request.user)
     return vendor



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def v_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('v_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance=vendor)


    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }

    return render(request, 'vendor/v_profile.html', context)


# function to build the menu
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    # get the categories for logged in vendors. To multiple query set we need filter
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


# food items show page
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
# to get the food items
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'fooditems': fooditems,
        'category': category,
       
    }
    return render(request, 'vendor/fooditems_by_category.html', context)
    

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            # now add the vendor part in the form
            category.vendor = get_vendor(request)
            # slugify will generate the slug based on category name
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "category added successfully")
            return redirect('menu_builder')
        
    else:
        form = CategoryForm()
        context = {
        'form': form,
        }
    return render(request, 'vendor/add_category.html', context)