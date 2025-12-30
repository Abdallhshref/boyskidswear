"""
Script to add B606 product to the database
Run with: python add_product_b606.py
"""

import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product, Color, Size, ProductVariant, Stock, Store, ProductImage

# Get or create category
category, _ = Category.objects.get_or_create(
    name="Baby Sets",
    defaults={'slug': 'baby-sets'}
)

# Create product
product, created = Product.objects.get_or_create(
    slug='pilot-kids-awesome-set-b606',
    defaults={
        'name': 'Pilot Kids Awesome Set B606',
        'description': 'Stylish "Pilot Kids Wear Awesome" teddy bear themed baby outfit set featuring a comfortable two-tone sweatshirt with cute bear print and matching pants with side stripe detail. Perfect for everyday wear, playtime, or casual outings. Made with soft, breathable fabric for your little one\'s comfort.',
        'category': category,
        'base_price': Decimal('450.00'),
        'main_image': 'products/B606/navy_main.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# Define colors with gradient (sleeve/pants, front panel)
color_data = [
    {'name': 'Navy & White', 'hex': '#1E3A5F,#FFFFFF'},
    {'name': 'Red & White', 'hex': '#DC143C,#FFFFFF'},
    {'name': 'Mauve & White', 'hex': '#C85A7E,#FFFFFF'},
]

# Get or create default store
store, _ = Store.objects.get_or_create(
    name="Main Store",
    defaults={'address': 'Cairo, Egypt'}
)

# Get existing sizes by name
sizes_to_use = []
for size_name in ['1', '2', '3']:
    size = Size.objects.filter(name=size_name).first()
    if size:
        sizes_to_use.append(size)

if not sizes_to_use:
    print("ERROR: No sizes found in database.")
    exit(1)

# Create colors, variants, and stock
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

# Add gallery images
gallery_images = [
    {'path': 'products/B606/red.jpg', 'alt': 'Red and White variant'},
    {'path': 'products/B606/mauve.jpg', 'alt': 'Mauve and White variant'},
]

for img_data in gallery_images:
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        image=img_data['path'],
        defaults={'alt_text': img_data['alt']}
    )
    if img_created:
        print(f"[OK] Added gallery image: {img_data['path']}")

print(f"\n[SUCCESS] Product B606 successfully added with {len(color_data)} colors and {len(sizes_to_use)} sizes!")
print(f"Total variants created: {len(color_data) * len(sizes_to_use)}")
