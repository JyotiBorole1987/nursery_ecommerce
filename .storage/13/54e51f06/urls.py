from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='store-home'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/category/<slug:category_slug>/', views.ProductListView.as_view(), name='category-products'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Cart URLs
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update-cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),
    
    # Wishlist URLs
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('remove-from-wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
    
    # Checkout URLs
    path('checkout/', views.checkout, name='checkout'),
    path('create-payment/', views.create_payment, name='create-payment'),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('order-complete/<int:order_id>/', views.order_complete, name='order-complete'),
    
    # Order URLs
    path('orders/', views.orders, name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order-detail'),
]