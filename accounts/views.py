from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User
from django.contrib import messages

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