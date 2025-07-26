from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category, SubCategory, Cart, Wishlist, Order, OrderItem, ProductImage
from .forms import ProductForm, ProductImageForm, UserRegistrationForm, SearchForm, FilterForm

def home(request):
    products = Product.objects.all()[:8]  
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories
    })

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    search_form = SearchForm()
    filter_form = FilterForm()
    
    # Search functionality
    if request.GET.get('query'):
        query = request.GET.get('query')
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        search_form = SearchForm(initial={'query': query})
    
    # Filter functionality
    if request.GET.get('category'):
        category_id = request.GET.get('category')
        products = products.filter(category_id=category_id)
        filter_form = FilterForm(initial={'category': category_id})
    
    if request.GET.get('price_range'):
        price_range = request.GET.get('price_range')
        if price_range == '0-100':
            products = products.filter(price__lte=100)
        elif price_range == '100-500':
            products = products.filter(price__gte=100, price__lte=500)
        elif price_range == '500-1000':
            products = products.filter(price__gte=500, price__lte=1000)
        elif price_range == '1000+':
            products = products.filter(price__gte=1000)
        filter_form = FilterForm(initial={'price_range': price_range})
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search_form': search_form,
        'filter_form': filter_form
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'is_in_wishlist': is_in_wishlist
    })

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/category_products.html', {
        'category': category,
        'page_obj': page_obj
    })

@login_required
def add_product(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to add products.')
        return redirect('home')
        
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.created_by = request.user
            product.save()
            
            # Handle multiple images properly
            images = request.FILES.getlist('image')
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            
            messages.success(request, 'Product added successfully!')
            return redirect('product_detail', slug=product.slug)
    else:
        product_form = ProductForm()
        image_form = ProductImageForm()
    
    return render(request, 'store/add_product.html', {
        'product_form': product_form,
        'image_form': image_form
    })

@login_required
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if not (request.user.is_staff or product.created_by == request.user):
        messages.error(request, 'You do not have permission to edit this product.')
        return redirect('product_detail', slug=product.slug)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'store/edit_product.html', {
        'form': form,
        'product': product
    })

@login_required
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if not (request.user.is_staff or product.created_by == request.user):
        messages.error(request, 'You do not have permission to delete this product.')
        return redirect('product_detail', slug=product.slug)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    
    return render(request, 'store/delete_product.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('product_detail', slug=product.slug)

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart_view')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart_view')
    
    total = sum(item.get_total_price() for item in cart_items)
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )
    
    # Create order items
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
    
    # Clear cart
    cart_items.delete()
    
    messages.success(request, f'Order #{order.id} placed successfully!')
    return redirect('order_history')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} added to wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist!')
    
    return redirect('product_detail', slug=product.slug)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = get_object_or_404(Wishlist, user=request.user, product=product)
    wishlist_item.delete()
    messages.success(request, f'{product.name} removed from wishlist!')
    return redirect('wishlist_view')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})
