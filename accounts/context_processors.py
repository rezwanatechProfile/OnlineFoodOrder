from vendor.models import Vendor


def get_vendor(request):
    # to avoid anonymous user use try and except. 
    try:
       vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)