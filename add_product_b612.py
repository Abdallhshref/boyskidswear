"""
Script to add B612 product to the database
"""

import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product, Color, Size, ProductVariant, Stock, Store, ProductImage

# Get Kids Girls category
category, _ = Category.objects.get_or_create(
    slug='kids-girls',
    defaults={'name': 'Kids Girls'}
)

# Create product
product, created = Product.objects.get_or_create(
    slug='the-pilot-girl-hoodie-set-b612',
    defaults={
        'name': 'The Pilot Girl Hoodie Set B612',
        'description': 'Stylish "The Pilot Girl" hoodie set featuring a comfortable hoodie with gradient detail and matching wide-leg pants. Perfect for everyday wear, playtime, or casual outings. Made with soft, breathable fabric for your little one\'s comfort.',
        'category': category,
        'base_price': Decimal('480.00'),
        'main_image': 'products/B612/burgundy_main.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# Define colors (solid colors for this product)
color_data = [
    {'name': 'Burgundy', 'hex': '#800020,#800020', 'img': 'burgundy_main.jpg'},
    {'name': 'Green', 'hex': '#3CB371,#3CB371', 'img': 'green.jpg'},
    {'name': 'Light Blue', 'hex': '#ADD8E6,#ADD8E6', 'img': 'lightblue.jpg'},
]

# Get or create default store
store, _ = Store.objects.get_or_create(
    name="Main Store",
    defaults={'address': 'Cairo, Egypt'}
)

# Get existing sizes
sizes_to_use = []
for size_name in ['1', '2', '3']:
    size = Size.objects.filter(name=size_name).first()
    if size:
        sizes_to_use.append(size)

if not sizes_to_use:
    print("ERROR: No sizes found.")
    exit(1)

# Create colors, variants, stock, and images
for color_info in color_data:
    color, color_created = Color.objects.get_or_create(
        name=color_info['name'],
        defaults={'hex_code': color_info['hex']}
    )
    
    if color_created:
        print(f"  [OK] Created color: {color.name}")
    
    for size in sizes_to_use:
        variant, variant_created = ProductVariant.objects.get_or_create(
            product=product,
            color=color,
            size=size,
            defaults={'additional_price': Decimal('0.00')}
        )
        
        if variant_created:
            print(f"    [OK] Created variant: {color.name} - Size {size.name}")
            
            Stock.objects.get_or_create(
                variant=variant,
                store=store,
                defaults={'quantity': 15}
            )
    
    img_path = f'products/B612/{color_info["img"]}'
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        image=img_path,
        defaults={'alt_text': f'{color.name} variant', 'color': color}
    )
    if img_created:
        print(f"[OK] Added image: {img_path} linked to {color.name}")

print(f"\n[SUCCESS] Product B612 added with {len(color_data)} colors!")
