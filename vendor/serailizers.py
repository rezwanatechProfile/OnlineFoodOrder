from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Vendor
from accounts.models import UserProfile
from menu.models import Category, FoodItem


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
      model = UserProfile
      fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'zip_code','latitude', 'longitude']


class VendorSerializer(serializers.ModelSerializer): 
    
    userprofile = UserProfileSerializer()   
    class Meta:
      model = Vendor
      fields = ['user', 'userprofile', 'vendor_name', 'vendor_slug', 'vendor_license', 'is_approved', 'created_at', 'modified_at']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
      model = Category
      fields = '__all__'


# class FoodItemSerializer(serializers.ModelSerializer):
#     class Meta:
#       model = FoodItem
#       fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']

