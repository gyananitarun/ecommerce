from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    
    # Product CRUD
    path('products/add/', views.add_product, name='add_product'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/edit/', views.edit_product, name='edit_product'),
    path('product/<slug:slug>/delete/', views.delete_product, name='delete_product'),
    
    # Cart
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Orders
    path('orders/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Authentication
    path('register/', views.register, name='register'),
]
