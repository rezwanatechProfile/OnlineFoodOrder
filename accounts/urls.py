from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    # path('registerUser/', views.UserView.as_view(), name='registerUser'),

    path('login/', views.login, name='login'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('custDashboard/', views.custDashboard, name='custDashboard'),

    # path('userupdate/', views.UserUpdate.as_view(), name='userupdate'),

    # path('activate/<uibd64>/<token>/', views.activate, name='activate'),

    path('vendor/', include('vendor.urls')),
    path('customer/', include('customers.urls')),
]

