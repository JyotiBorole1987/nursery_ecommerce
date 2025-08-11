import os
import django
import random
from django.utils import timezone
from django.core.files.images import ImageFile
from django.contrib.auth.models import User

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_nursery.settings')
django.setup()

from store.models import Category, Product
from users.models import Profile, Wishlist

def create_sample_data():
    print("Creating sample data for Green Oasis Nursery...")
    
    # Create superuser
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser created: admin / admin123")
    
    # Create categories
    categories = [
        {
            'name': 'Indoor Plants',
            'slug': 'indoor-plants',
            'description': 'Beautiful plants that thrive indoors. Perfect for adding greenery to your home.'
        },
        {
            'name': 'Outdoor Plants',
            'slug': 'outdoor-plants',
            'description': 'Hardy plants that flourish in gardens, patios, and outdoor spaces.'
        },
        {
            'name': 'Succulents',
            'slug': 'succulents',
            'description': 'Low-maintenance plants with water-storing capabilities, perfect for beginners.'
        },
        {
            'name': 'Fruit Trees',
            'slug': 'fruit-trees',
            'description': 'Trees that produce delicious fruits for your home garden.'
        },
        {
            'name': 'Flower Plants',
            'slug': 'flower-plants',
            'description': 'Plants that produce beautiful blooms to brighten your space.'
        },
        {
            'name': 'Herb Plants',
            'slug': 'herb-plants',
            'description': 'Aromatic and flavorful herbs for cooking and medicinal purposes.'
        },
    ]
    
    created_categories = []
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description']
            }
        )
        created_categories.append(category)
        if created:
            print(f"Created category: {category.name}")
    
    # Create sample products
    products = [
        # Indoor Plants
        {
            'name': 'Peace Lily',
            'slug': 'peace-lily',
            'category': 'indoor-plants',
            'description': 'The Peace Lily (Spathiphyllum) is an easy-care plant with elegant white flowers. It thrives in low light conditions and helps purify indoor air.',
            'price': 24.99,
            'stock': 50,
            'featured': True
        },
        {
            'name': 'Snake Plant',
            'slug': 'snake-plant',
            'category': 'indoor-plants',
            'description': 'The Snake Plant (Sansevieria) is virtually indestructible and perfect for beginners. Its tall, architectural leaves add modern style to any room.',
            'price': 19.99,
            'stock': 45,
            'featured': True
        },
        {
            'name': 'Pothos',
            'slug': 'pothos',
            'category': 'indoor-plants',
            'description': 'Pothos (Epipremnum aureum) is a trailing vine with heart-shaped leaves. It\'s extremely adaptable and can thrive in various light conditions.',
            'price': 15.99,
            'stock': 60,
            'featured': False
        },
        
        # Outdoor Plants
        {
            'name': 'Hydrangea',
            'slug': 'hydrangea',
            'category': 'outdoor-plants',
            'description': 'Hydrangeas produce large, showy flower heads in blue, pink, or white. They thrive in partial shade and moist, well-drained soil.',
            'price': 29.99,
            'stock': 35,
            'featured': True
        },
        {
            'name': 'Lavender',
            'slug': 'lavender',
            'category': 'outdoor-plants',
            'description': 'Lavender is a fragrant herb with beautiful purple flowers. It attracts pollinators and thrives in sunny, dry conditions.',
            'price': 12.99,
            'stock': 55,
            'featured': False
        },
        {
            'name': 'Japanese Maple',
            'slug': 'japanese-maple',
            'category': 'outdoor-plants',
            'description': 'Japanese Maple (Acer palmatum) is a small, ornamental tree known for its stunning red foliage and elegant branching pattern.',
            'price': 89.99,
            'stock': 20,
            'featured': True
        },
        
        # Succulents
        {
            'name': 'Aloe Vera',
            'slug': 'aloe-vera',
            'category': 'succulents',
            'description': 'Aloe Vera is known for its medicinal properties. The gel inside its thick, fleshy leaves can soothe skin irritations and burns.',
            'price': 14.99,
            'stock': 75,
            'featured': True
        },
        {
            'name': 'Echeveria',
            'slug': 'echeveria',
            'category': 'succulents',
            'description': 'Echeveria forms stunning geometric rosettes in a variety of colors. It\'s perfect for sunny windowsills and requires minimal watering.',
            'price': 9.99,
            'stock': 80,
            'featured': False
        },
        {
            'name': 'Jade Plant',
            'slug': 'jade-plant',
            'category': 'succulents',
            'description': 'The Jade Plant (Crassula ovata) is a popular houseplant with thick branches and oval-shaped leaves. It symbolizes good luck and prosperity.',
            'price': 17.99,
            'stock': 65,
            'featured': False
        },
        
        # Fruit Trees
        {
            'name': 'Meyer Lemon Tree',
            'slug': 'meyer-lemon-tree',
            'category': 'fruit-trees',
            'description': 'The Meyer Lemon Tree produces sweet-tart lemons year-round. It can be grown indoors or outdoors in warmer climates.',
            'price': 59.99,
            'stock': 25,
            'featured': True
        },
        {
            'name': 'Dwarf Apple Tree',
            'slug': 'dwarf-apple-tree',
            'category': 'fruit-trees',
            'description': 'Dwarf Apple Trees produce full-sized apples but on a smaller tree, perfect for small gardens or containers.',
            'price': 49.99,
            'stock': 30,
            'featured': False
        },
        {
            'name': 'Fig Tree',
            'slug': 'fig-tree',
            'category': 'fruit-trees',
            'description': 'Fig Trees produce sweet, delicious fruits and have attractive lobed leaves. They can be grown in containers or in the ground.',
            'price': 54.99,
            'stock': 28,
            'featured': False
        },
        
        # Flower Plants
        {
            'name': 'Rose Bush',
            'slug': 'rose-bush',
            'category': 'flower-plants',
            'description': 'Classic roses known for their beautiful blooms and lovely fragrance. Available in various colors to brighten any garden.',
            'price': 34.99,
            'stock': 40,
            'featured': True
        },
        {
            'name': 'Sunflower',
            'slug': 'sunflower',
            'category': 'flower-plants',
            'description': 'Sunflowers are known for their large, cheerful blooms that track the sun. They\'re easy to grow and attract birds and pollinators.',
            'price': 8.99,
            'stock': 100,
            'featured': False
        },
        {
            'name': 'Tulip Bulbs',
            'slug': 'tulip-bulbs',
            'category': 'flower-plants',
            'description': 'Tulips produce elegant, cup-shaped flowers in spring. Plant the bulbs in fall for a colorful display next year.',
            'price': 12.99,
            'stock': 150,
            'featured': False
        },
        
        # Herb Plants
        {
            'name': 'Basil',
            'slug': 'basil',
            'category': 'herb-plants',
            'description': 'Basil is an aromatic herb with sweet, slightly peppery flavor. Perfect for cooking, especially in Italian dishes.',
            'price': 7.99,
            'stock': 85,
            'featured': True
        },
        {
            'name': 'Mint',
            'slug': 'mint',
            'category': 'herb-plants',
            'description': 'Mint is a versatile herb with a refreshing flavor. Great for teas, cocktails, and various culinary uses.',
            'price': 7.99,
            'stock': 90,
            'featured': False
        },
        {
            'name': 'Rosemary',
            'slug': 'rosemary',
            'category': 'herb-plants',
            'description': 'Rosemary is an aromatic evergreen herb with needle-like leaves. It has a pine-like fragrance and flavor.',
            'price': 8.99,
            'stock': 75,
            'featured': False
        },
    ]
    
    for prod_data in products:
        category = Category.objects.get(slug=prod_data['category'])
        product, created = Product.objects.get_or_create(
            slug=prod_data['slug'],
            defaults={
                'name': prod_data['name'],
                'category': category,
                'description': prod_data['description'],
                'price': prod_data['price'],
                'stock': prod_data['stock'],
                'featured': prod_data['featured'],
                'available': True,
                # Using a placeholder image since we can't upload real images in this setup
                'image': 'products/placeholder.jpg'
            }
        )
        if created:
            print(f"Created product: {product.name}")
    
    print("Sample data creation complete!")

if __name__ == "__main__":
    create_sample_data()