"""
Script to add B614 product to the database
"""

import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product, Color, Size, ProductVariant, Stock, Store, ProductImage

# Get Kids Boys category
category, _ = Category.objects.get_or_create(
    slug='kids-boys',
    defaults={'name': 'Kids Boys'}
)

# Create product
product, created = Product.objects.get_or_create(
    slug='pilot-texture-hoodie-set-b614',
    defaults={
        'name': 'Pilot Texture Hoodie Set B614',
        'description': 'Premium textured hoodie set featuring a "PILOT" patch design with textured text on sleeves. Includes a comfortable hoodie with kangaroo pocket and matching textured joggers with side print. Stylish and durable for active kids.',
        'category': category,
        'base_price': Decimal('520.00'),
        'main_image': 'products/B614/cream_main.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# Define colors
color_data = [
    {'name': 'Cream & Beige', 'hex': '#FDFDD0,#F5F5DC', 'img': 'cream_main.jpg'},
    {'name': 'Grey', 'hex': '#808080,#808080', 'img': 'grey.jpg'},
    {'name': 'Mint Green', 'hex': '#98FF98,#98FF98', 'img': 'mint.jpg'},
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
    
    img_path = f'products/B614/{color_info["img"]}'
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        image=img_path,
        defaults={'alt_text': f'{color.name} variant', 'color': color}
    )
    if img_created:
        print(f"[OK] Added image: {img_path} linked to {color.name}")

print(f"\n[SUCCESS] Product B614 added with {len(color_data)} colors!")
