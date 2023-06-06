from django.shortcuts import render
from vendor.models import Vendor
from rest_framework.decorators import api_view
from rest_framework.response import Response
from vendor.serailizers import VendorSerializer


def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    print(vendors)
    context = {
        'vendors': vendors
    }
    return render(request, 'home.html', context)

# @api_view(['GET'])
# def home(request):
#     vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
#     serializer = VendorSerializer(vendors, many=True)

#     context = {
#         'vendors': vendors
#     }
#     return Response(serializer.data)