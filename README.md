# Django eCommerce Store

A complete eCommerce solution built with Django, featuring product management, shopping cart, user authentication, wishlist, and order tracking.

## Features

### ✅ Completed Features
- **User Authentication**: Registration, Login, Logout
- **Product Management**: CRUD operations for products
- **Categories & Subcategories**: Organized product catalog
- **Shopping Cart**: Add, remove, update quantities
- **Wishlist**: Save products for later
- **Order Management**: Checkout and order history
- **Search & Filters**: Search by name, filter by category and price
- **Admin Panel**: Fully customized Django admin
- **Responsive Design**: Clean HTML/CSS interface

### 🏗️ Project Structure
```
ecommerce/
├── ecommerce/          # Main project settings
├── store/              # Main app
│   ├── models.py       # Database models
│   ├── views.py        # Business logic
│   ├── forms.py        # Form definitions
│   ├── admin.py        # Admin customization
│   └── urls.py         # URL routing
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── store/          # Store templates
│   └── registration/   # Auth templates
├── static/css/         # CSS styles
└── media/              # User uploads
```

## Quick Start

### 1. Setup Virtual Environment (Recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install django pillow
```

### 3. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Create Sample Data (Optional)
```bash
python manage.py create_sample_data
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the site.

## Models Overview

### Core Models
- **Category**: Product categories with images and slugs
- **SubCategory**: Nested categories under main categories
- **Product**: Main product model with all details
- **ProductImage**: Multiple images per product

### User Interaction Models
- **Cart**: Shopping cart items for users
- **Wishlist**: Saved products for later
- **Order**: Order header with status tracking
- **OrderItem**: Individual items within orders

## Key Features Explained

### 1. Product Management
- Add, edit, delete products (authenticated users)
- Automatic slug generation
- Image upload support
- Stock tracking
- Category-based organization

### 2. Shopping Experience
- Add products to cart
- Update quantities
- Remove items
- Secure checkout process
- Order confirmation and tracking

### 3. Search & Discovery
- Text search across product names and descriptions
- Category-based filtering
- Price range filters
- Pagination for large product lists

### 4. User Features
- User registration and authentication
- Personal shopping cart
- Wishlist functionality
- Order history tracking
- Product management for sellers

## Admin Panel Features
- Product management with inline image uploads
- Category and subcategory management
- Order tracking and status updates
- User management
- Search and filter capabilities

## URLs Structure
```
/                           # Home page
/products/                  # Product listing
/products/add/              # Add new product
/product/<slug>/            # Product detail
/category/<slug>/           # Category products
/cart/                      # Shopping cart
/checkout/                  # Checkout process
/orders/                    # Order history
/wishlist/                  # User wishlist
/login/                     # User login
/register/                  # User registration
/admin/                     # Admin panel
```

## Technologies Used
- **Backend**: Django 5.1
- **Database**: SQLite (development)
- **Frontend**: HTML5, CSS3
- **Image Processing**: Pillow
- **Authentication**: Django built-in auth

## Development Notes

### Database
- Uses SQLite for development (easy setup)
- Can be easily switched to PostgreSQL/MySQL for production

### Static Files
- CSS files in `/static/css/`
- Media files uploaded to `/media/`

### Security
- CSRF protection enabled
- User authentication required for sensitive operations
- Input validation on all forms

## Future Enhancements
- Payment gateway integration
- Email notifications
- Product reviews and ratings
- Advanced inventory management
- API endpoints for mobile apps

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License
This project is for educational purposes.
