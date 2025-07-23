from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, SubCategory, Product, ProductImage

class Command(BaseCommand):
    help = 'Create sample data for the eCommerce store'

    def handle(self, *args, **options):
        # Create test user if doesn't exist
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )
            self.stdout.write(f'Created user: {user.username}')
        else:
            user = User.objects.get(username='testuser')

        # Create categories
        categories_data = [
            {'name': 'Electronics', 'subcategories': ['Smartphones', 'Laptops', 'Headphones']},
            {'name': 'Clothing', 'subcategories': ['Men', 'Women', 'Kids']},
            {'name': 'Books', 'subcategories': ['Fiction', 'Non-Fiction', 'Educational']},
            {'name': 'Home & Garden', 'subcategories': ['Furniture', 'Decor', 'Tools']},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(name=cat_data['name'])
            if created:
                self.stdout.write(f'Created category: {category.name}')
            
            for subcat_name in cat_data['subcategories']:
                subcategory, created = SubCategory.objects.get_or_create(
                    name=subcat_name,
                    category=category
                )
                if created:
                    self.stdout.write(f'Created subcategory: {subcategory.name}')

        # Create sample products
        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'price': 999.99,
                'description': 'Latest iPhone with advanced features and premium build quality.',
                'category': 'Electronics',
                'subcategory': 'Smartphones',
                'stock': 50
            },
            {
                'name': 'MacBook Air M2',
                'price': 1199.99,
                'description': 'Powerful and lightweight laptop perfect for work and creativity.',
                'category': 'Electronics',
                'subcategory': 'Laptops',
                'stock': 25
            },
            {
                'name': 'Sony WH-1000XM4',
                'price': 349.99,
                'description': 'Premium noise-canceling wireless headphones.',
                'category': 'Electronics',
                'subcategory': 'Headphones',
                'stock': 75
            },
            {
                'name': 'Classic Denim Jacket',
                'price': 79.99,
                'description': 'Timeless denim jacket suitable for all seasons.',
                'category': 'Clothing',
                'subcategory': 'Men',
                'stock': 100
            },
            {
                'name': 'Summer Floral Dress',
                'price': 59.99,
                'description': 'Beautiful floral dress perfect for summer occasions.',
                'category': 'Clothing',
                'subcategory': 'Women',
                'stock': 80
            },
            {
                'name': 'Python Programming Book',
                'price': 39.99,
                'description': 'Comprehensive guide to Python programming for beginners.',
                'category': 'Books',
                'subcategory': 'Educational',
                'stock': 200
            }
        ]

        for product_data in products_data:
            category = Category.objects.get(name=product_data['category'])
            subcategory = SubCategory.objects.get(
                name=product_data['subcategory'],
                category=category
            )
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'price': product_data['price'],
                    'description': product_data['description'],
                    'category': category,
                    'subcategory': subcategory,
                    'stock': product_data['stock'],
                    'created_by': user
                }
            )
            
            if created:
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
