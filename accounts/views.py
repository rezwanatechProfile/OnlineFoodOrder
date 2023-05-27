from django.shortcuts import redirect, render
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User
from .signals import UserProfile
from django.contrib import messages, auth
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def registerUser(request):
    if request.method == 'POST':
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


def registerVendor(request):

    if request.method == 'POST':
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
            # vendor_name = v_form.cleaned_data['vendor_name']
            # vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            try:
                userprofile = UserProfile.objects.get(user=user)
                vendor.userprofile = userprofile
                vendor.save()
            except:
                UserProfile.DoesNotExist
                print("no matching userprofile")


            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            # send_verification_email(request, user, mail_subject, email_template)

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



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid loging credentials')
            return redirect('login')


    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out")
    return redirect('login')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')


