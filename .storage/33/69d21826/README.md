# Green Oasis Nursery - E-commerce Plant Shop

A full-featured Django e-commerce website for a plant and tree nursery. The platform allows customers to browse, purchase, and manage plants, trees, and garden products.

## Features

- **User Authentication**: Registration, login, profile management
- **Product Catalog**: Categorized products with detailed descriptions
- **Shopping Cart**: Add, update, remove items
- **Wishlist**: Save products for future reference
- **Checkout Process**: Seamless checkout with Stripe payment integration
- **Order Management**: Track and manage orders
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Backend**: Python 3.10, Django 5.2
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 4
- **Database**: SQLite (default), supports PostgreSQL for production
- **Payment Processing**: Stripe API
- **Additional Packages**: Pillow, django-crispy-forms

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd plant_nursery_ecommerce
   ```

2. Create and activate virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Create sample data (optional):
   ```
   python sample_data.py
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Access the website at `http://127.0.0.1:8000/`

## Configuration

### Stripe Integration

For payment processing to work, you need to set up Stripe:

1. Create a Stripe account at https://stripe.com
2. Get your API keys from the Stripe dashboard
3. Update the following settings in `plant_nursery/settings.py`:
   ```python
   STRIPE_PUBLIC_KEY = 'your_stripe_public_key'
   STRIPE_SECRET_KEY = 'your_stripe_secret_key'
   STRIPE_WEBHOOK_SECRET = 'your_stripe_webhook_secret'
   ```

## Project Structure

```
plant_nursery_ecommerce/
├── plant_nursery/         # Project settings
├── store/                 # Store app (products, cart, orders)
├── users/                 # User authentication and profiles
├── static/                # Static files (CSS, JS)
├── media/                 # User-uploaded media files
├── templates/             # HTML templates
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Admin Access

Access the admin panel at `http://127.0.0.1:8000/admin/` using your superuser credentials.

From there you can manage:
- Products and categories
- User accounts
- Orders and payments
- Wishlist items

## Development

### Adding New Products

1. Log in to the admin interface
2. Navigate to Products > Add Product
3. Fill in the product details
4. Upload a product image
5. Save the product

### Creating Categories

1. Log in to the admin interface
2. Navigate to Categories > Add Category
3. Fill in the category name and description
4. Save the category

## Production Deployment

For production deployment, make sure to:

1. Set `DEBUG = False` in settings
2. Configure a production-ready database (PostgreSQL recommended)
3. Set up proper static and media file serving
4. Configure HTTPS with a valid SSL certificate
5. Set proper environment variables for secrets

## License

This project is licensed under the MIT License - see the LICENSE file for details.