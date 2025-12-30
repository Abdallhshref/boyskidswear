"""
Script to add B605 product to the database
Run with: python add_product_b605.py
"""

import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product, Color, Size, ProductVariant, Stock, Store

# Get or create category
category, _ = Category.objects.get_or_create(
    name="Baby Sets",
    defaults={'slug': 'baby-sets'}
)

# Create product
product, created = Product.objects.get_or_create(
    slug='love-mom-butterfly-set-b605',
    defaults={
        'name': 'Love Mom Butterfly Set B605',
        'description': 'Adorable "Love Mom" butterfly-themed baby outfit set featuring a comfortable sweatshirt with sequined bow design and matching pants. Perfect for everyday wear, playtime, or casual outings. Made with soft, breathable fabric for your little one\'s comfort.',
        'category': category,
        'base_price': Decimal('450.00'),
        'main_image': 'products/B605/lavender_main.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# Define colors with gradient (top,pants)
color_data = [
    {'name': 'Lavender & Mauve', 'hex': '#DDA0DD,#C85A7E'},
    {'name': 'Sky Blue & Hot Pink', 'hex': '#87CEEB,#FF69B4'},
    {'name': 'Peach & Turquoise', 'hex': '#FFDAB9,#40E0D0'},
]

# Get or create default store
store, _ = Store.objects.get_or_create(
    name="Main Store",
    defaults={'address': 'Cairo, Egypt'}
)

# Get existing sizes by name
sizes_to_use = []
for size_name in ['1', '2', '3']:
    try:
        size = Size.objects.filter(name=size_name).first()
        if size:
            sizes_to_use.append(size)
    except Size.DoesNotExist:
        print(f"Warning: Size '{size_name}' not found")

if not sizes_to_use:
    print("ERROR: No sizes found in database. Please add sizes first.")
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
        # Create variant
        variant, variant_created = ProductVariant.objects.get_or_create(
            product=product,
            color=color,
            size=size,
            defaults={'additional_price': Decimal('0.00')}
        )
        
        if variant_created:
            print(f"    [OK] Created variant: {color.name} - Size {size.name}")
            
            # Add stock  
            Stock.objects.get_or_create(
                variant=variant,
                store=store,
                defaults={'quantity': 15}
            )

print(f"\n[SUCCESS] Product B605 successfully added with {len(color_data)} colors and {len(sizes_to_use)} sizes!")
print(f"Total variants created: {len(color_data) * len(sizes_to_use)}")
