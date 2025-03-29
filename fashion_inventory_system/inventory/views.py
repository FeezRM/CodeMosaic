from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Product, User
from .forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm,
    ProductForm,
    ProductFilterForm
)
from django.contrib import messages
from django.http import JsonResponse

# Authentication Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'product_list')
            return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'inventory/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'inventory/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def guest_view(request):
    # Guest users can only view products
    request.session['guest_mode'] = True
    return redirect('product_list')

# Product Views
class ProductListView(ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Convert to list and sort numerically by product_id
        queryset = sorted(list(queryset), key=lambda x: int(x.product_id))
        
        # Apply filters
        filters = {}
        for field in ['brand', 'category', 'color', 'size']:
            if value := self.request.GET.get(field):
                filters[field] = value
        if price_min := self.request.GET.get('price_min'):
            queryset = [p for p in queryset if float(p.price) >= float(price_min)]
        if price_max := self.request.GET.get('price_max'):
            queryset = [p for p in queryset if float(p.price) <= float(price_max)]
        if filters:
            queryset = [p for p in queryset if all(p.__dict__[key] == value for key, value in filters.items())]
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProductFilterForm(self.request.GET or None)
        context['search_query'] = self.request.GET.get('search', '')
        context['is_guest'] = self.request.session.get('guest_mode', False)
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')
    login_url = '/login/'
    
    def form_valid(self, form):
        messages.success(self.request, "Product added successfully!")
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')
    login_url = '/login/'

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    login_url = '/login/'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, 'Product deleted successfully!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        return super().delete(request, *args, **kwargs)

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'can_edit': not request.session.get('guest_mode', False)
    }
    return render(request, 'inventory/product_detail.html', context)

# Dashboard View
@login_required
def dashboard(request):
    if request.session.get('guest_mode', False):
        return redirect('product_list')
        
    products = Product.objects.all()
    total_products = products.count()
    low_stock = products.filter(stock_quantity__lt=10).count()
    total_value = sum(p.price * p.stock_quantity for p in products)
    
    context = {
        'total_products': total_products,
        'low_stock': low_stock,
        'total_value': round(total_value, 2),
        'recent_products': products.order_by('-id')[:5]
    }
    
    return render(request, 'inventory/dashboard.html', context)