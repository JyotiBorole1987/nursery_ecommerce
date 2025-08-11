from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Product, Category, CartItem, Order, OrderItem, WishlistItem
from users.models import Wishlist
import stripe
import json


stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    featured_products = Product.objects.filter(featured=True)[:6]
    categories = Category.objects.all()[:6]
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'title': 'Home'
    }
    return render(request, 'store/home.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        search_query = self.request.GET.get('q')
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        
        search_query = self.request.GET.get('q')
        if search_query:
            context['search_query'] = search_query
            
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['related_products'] = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]
        
        # Check if product is in wishlist
        if self.request.user.is_authenticated:
            try:
                wishlist = Wishlist.objects.get(user=self.request.user)
                context['in_wishlist'] = WishlistItem.objects.filter(
                    wishlist=wishlist, 
                    product=product
                ).exists()
            except Wishlist.DoesNotExist:
                context['in_wishlist'] = False
        return context


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart')


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'title': 'Shopping Cart'
    }
    return render(request, 'store/cart.html', context)


@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        action = request.POST.get('action')
        
        if action == 'increase':
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
                cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        
        return redirect('cart')
    
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, f"{cart_item.product.name} removed from your cart.")
    return redirect('cart')


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    wishlist_item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )
    
    if created:
        messages.success(request, f"{product.name} added to your wishlist.")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")
    
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('product-detail', slug=product.slug)


@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
    product_name = wishlist_item.product.name
    wishlist_item.delete()
    messages.success(request, f"{product_name} removed from your wishlist.")
    
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('wishlist')


@login_required
def wishlist(request):
    try:
        user_wishlist = Wishlist.objects.get(user=request.user)
        wishlist_items = WishlistItem.objects.filter(wishlist=user_wishlist)
    except Wishlist.DoesNotExist:
        wishlist_items = []
    
    context = {
        'wishlist_items': wishlist_items,
        'title': 'My Wishlist'
    }
    return render(request, 'store/wishlist.html', context)


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items:
        messages.warning(request, "Your cart is empty. Add some products before checkout.")
        return redirect('cart')
    
    total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'title': 'Checkout'
    }
    return render(request, 'store/checkout.html', context)


@login_required
def create_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_items = CartItem.objects.filter(user=request.user)
        
        if not cart_items:
            return JsonResponse({'error': 'Your cart is empty'}, status=400)
        
        total_amount = int(sum(item.total_price for item in cart_items) * 100)  # Convert to cents for Stripe
        
        try:
            # Create payment intent with Stripe
            intent = stripe.PaymentIntent.create(
                amount=total_amount,
                currency='usd',
                metadata={
                    'user_id': request.user.id
                }
            )
            
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def payment_success(request):
    if request.method == 'POST':
        payment_intent_id = request.POST.get('payment_intent_id')
        shipping_data = {
            'full_name': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            'zip_code': request.POST.get('zip_code'),
            'phone': request.POST.get('phone')
        }
        
        cart_items = CartItem.objects.filter(user=request.user)
        total_amount = sum(item.total_price for item in cart_items)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=shipping_data['full_name'],
            email=shipping_data['email'],
            address=shipping_data['address'],
            city=shipping_data['city'],
            state=shipping_data['state'],
            zip_code=shipping_data['zip_code'],
            phone=shipping_data['phone'],
            total_amount=total_amount,
            payment_id=payment_intent_id,
            payment_status=True,
            status='processing'
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )
            
            # Update product stock
            product = cart_item.product
            product.stock -= cart_item.quantity
            if product.stock <= 0:
                product.available = False
            product.save()
        
        # Clear the cart
        cart_items.delete()
        
        messages.success(request, "Your order has been placed successfully!")
        return redirect('order-complete', order_id=order.id)
    
    return redirect('checkout')


@login_required
def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'order_items': order_items,
        'title': 'Order Complete'
    }
    return render(request, 'store/order_complete.html', context)


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': user_orders,
        'title': 'My Orders'
    }
    return render(request, 'store/orders.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'order_items': order_items,
        'title': f'Order #{order.id}'
    }
    return render(request, 'store/order_detail.html', context)