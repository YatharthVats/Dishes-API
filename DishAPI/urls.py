"""DishAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from order.views import login,create_user,display_dishes,display_customers,create_dish,display_particular_customers,add_dish,delete_dish


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', login),
    path('api/signup', create_user),
    path('api/createdish',create_dish),
    path('api/dishes',display_dishes),
    path('api/customers',display_customers),
    path('api/customer/',display_particular_customers),
    path('api/dishadd',add_dish),
    path('api/dishdelete',delete_dish),
]
