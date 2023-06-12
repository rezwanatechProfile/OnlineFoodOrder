from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Vendor
from accounts.models import User, UserProfile
from menu.models import Category, FoodItem
from marketplace.models import Cart




class Vendor_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone_number']

class Customer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone_number']

class UserSerializer(serializers.Serializer):  
    
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        role_value = obj.role
        if role_value == 1:
            user_role = 'Vendor'
            serializer = Vendor_Serializer(obj)  # Replace with your actual Vendor_Serializer
        elif role_value == 2:
            user_role = 'Customer'
            serializer = Customer_Serializer(obj)  # Replace with your actual Customer_Serializer
        else:
            user_role = 'Unknown'
            serializer = None

        if serializer is not None:
            return {
                'role': user_role,
                'data': serializer.data
            }
        else:
            return {
                'role': user_role
            }

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'phone_number', 'role']
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    # def to_representation(self, instance):
    #     serializer = self.get_role_serializer(instance)
    #     return serializer.data

    # def get_role_serializer(self, instance):
    #     role_value = instance.role
    #     if role_value == 1:
    #         serializer = Vendor_Serializer(instance)
    #     elif role_value == 2:
    #         serializer = Customer_Serializer(instance)
    #     else:
    #         raise serializers.ValidationError("Invalid user role.")
    #     return serializer
    


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
      model = UserProfile
      fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'zip_code','latitude', 'longitude']
      read_only_fields = ['user']
    
    def validate(self,attrs):
        attrs['user'] = self.context['request'].user
        return attrs
    # To show the details of user (Overwriting)
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        print(instance.user.role)
        return response


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
      model = FoodItem
      fields = ['vendor', 'category', 'food_title', 'description', 'price', 'image', 'is_available']


    # def __init__(self, *arg, **kwargs):
    #     super(FoodItemSerializer, self).__init__(*arg, **kwargs)
    #     self.Meta.depth = 1



class CategorySerializer(serializers.ModelSerializer):
    fooditems = FoodItemSerializer(many=True, read_only=True)
    class Meta:
      model = Category
      fields = ['vendor', 'category_name', 'description', 'fooditems']

class VendorSerializer(serializers.ModelSerializer): 
    categories = CategorySerializer(many=True, read_only=True)
    userprofile = UserProfileSerializer()   
    class Meta:
      model = Vendor
      fields = ['categories', 'user', 'userprofile', 'vendor_name', 'vendor_slug', 'vendor_license', 'is_approved', 'created_at', 'modified_at']



class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    fooditem = FoodItemSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'fooditem', 'quantity', 'created_at', 'updated_at']


# class AddToCartSerializer(serializers.Serializer):
#     status = serializers.CharField()
#     message = serializers.CharField()
#     cart_counter = serializers.IntegerField()
#     qty = serializers.IntegerField()
#     cart_amount = serializers.FloatField()

    # def to_representation(self, instance):
    #     cart_count = instance.get('cart_count', 0)
    #     subtotal = instance.get('subtotal', 0)
    #     tax = instance.get('tax', 0)
    #     grand_total = instance.get('grand_total', 0)

    #     representation = super(AddToCartSerializer, self).to_representation(instance)
    #     representation['cart_counter'] = cart_count
    #     representation['cart_amount'] = grand_total
    #     return representation