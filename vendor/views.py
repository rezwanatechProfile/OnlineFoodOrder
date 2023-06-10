from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import UserProfile
from menu.forms import CategoryForm, FoodItemForm
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


# Vendor profile / Dashboard function

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



# function to build the menu (Category and food items)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    # get the categories for logged in vendors. To multiple query set we need filter. Use Order_by to show the edited or added items first in the list.
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
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
    


# CRUD Application of Category

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            # now add the vendor part in the form
            category.vendor = get_vendor(request)
            # slugify will generate the slug based on category name
            # category.save() will generate the id
            category.save() 
            category.slug = slugify(category_name)+'-'+str(category.id)
            category.save()

            messages.success(request, "Category added successfully")
            return redirect('menu_builder')
        else:
            print(form.errors)
        
    else:
        form = CategoryForm()
    context = {
        'form': form,
        }
    return render(request, 'vendor/add_category.html', context)




# edit functions
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    # create category instance and should be pass inside the form. Instance create the existing data in the form.
     category = get_object_or_404(Category, pk=pk)
     if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            # now add the vendor part in the form
            category.vendor = get_vendor(request)
            # slugify will generate the slug based on category name
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "category Updated Successfully")
            return redirect('menu_builder')
        else:
            print(form.errors)
        
     else:
        form = CategoryForm(instance=category)
     context = {
        'form': form,
        'category': category,
        }
     return render(request, 'vendor/edit_category.html', context)


def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "category has been deleted Successfully")
    return redirect('menu_builder')
    
    

# CRUD Application of Food Items

def add_food(request):
     if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            # now add the vendor part in the form
            food.vendor = get_vendor(request)
            # slugify will generate the slug based on category name
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request, "Food Item added successfully")
            return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)
        
     else:
        form = FoodItemForm()
        # to get the each owner's categories in category filter
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
     context = {
        'form': form,
        }
     return render(request, 'vendor/add_food.html', context)


# edit FoodItem functions
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    # create category instance and should be pass inside the form. Instance create the existing data in the form.
     foodItem = get_object_or_404(FoodItem, pk=pk)
     if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=foodItem)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            foodItem = form.save(commit=False)
            # now add the vendor part in the form
            foodItem.vendor = get_vendor(request)
            # slugify will generate the slug based on category name
            foodItem.slug = slugify(foodtitle)
            form.save()
            messages.success(request, "Food Item Updated Successfully")
            return redirect('fooditems_by_category', foodItem.category.id)
        else:
            print(form.errors)
        
     else:
        form = FoodItemForm(instance=foodItem)
     context = {
        'form': form,
        'foodItem': foodItem,
        }
     return render(request, 'vendor/edit_food.html', context)


def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, "Food Item has been deleted Successfully")
    return redirect('menu_builder')