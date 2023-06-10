from rest_framework import serializers
from .models import Category, FoodItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
      model = Category
      fields = ['category_name', 'description']


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
      model = FoodItem
      fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available']