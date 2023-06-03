from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.v_profile, name='v_profile'),
  # path for menu builder
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>', views.fooditems_by_category, name='fooditems_by_category'),
    
  # Category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    
    
]