from .models import UserProfile
from vendor.models import Vendor
from django.conf import settings

# To make vendor object available in every pages. For example: cover.html
def get_vendor(request):
    # to avoid anonymous user use try and except. 
    try:
       vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


def get_user_profile(request):
    # to avoid anonymous user use try and except. 
    try:
       userprofile = UserProfile.objects.get(user=request.user)
    except:
        userprofile = None
    return dict(userprofile=userprofile)



def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}


# After writing functions in context.processors register in settings.py