"""
URL configuration for fashion_inventory_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from inventory import views
from inventory.views import ProductCreateView, ProductDeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/add/', login_required(views.ProductCreateView.as_view()), name='product_create'),
    path('product/<int:pk>/edit/', login_required(views.ProductUpdateView.as_view()), name='product_update'),
    path('product/<int:pk>/delete/', login_required(views.ProductDeleteView.as_view()), name='product_delete'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
