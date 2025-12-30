"""
Script to add B601 product to the database
Run with: python add_product_b601.py
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
    slug='hello-dino-set-b601',
    defaults={
        'name': 'Hello Dino Set B601',
        'description': 'Adorable "Hello" dinosaur themed baby outfit set featuring a comfortable sweatshirt with 3D dino character and matching pants with dinosaur spike detail. Perfect for everyday wear, playtime, or casual outings. Made with soft, breathable fabric for your little one\'s comfort.',
        'category': category,
        'base_price': Decimal('450.00'),
        'main_image': 'products/B601/orange_main.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# Define colors with gradient (top, pants)
color_data = [
    {'name': 'Orange & Blue', 'hex': '#FFA500,#6495ED', 'img': 'orange_main.jpg'},
    {'name': 'Yellow & Navy', 'hex': '#FFD700,#191970', 'img': 'yellow.jpg'},
    {'name': 'Pink & Black', 'hex': '#FFB6C1,#000000', 'img': 'pink.jpg'},
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

# Create colors, variants, stock, and images
for color_info in color_data:
    # Check if color exists with this name for this product (may need different names for same color combos)
    color, color_created = Color.objects.get_or_create(
        name=color_info['name'],
        defaults={'hex_code': color_info['hex']}
    )
    
    # Update hex if it was different
    if not color_created and color.hex_code != color_info['hex']:
        color.hex_code = color_info['hex']
        color.save()
    
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
    
    # Add product image linked to color
    img_path = f'products/B601/{color_info["img"]}'
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        image=img_path,
        defaults={'alt_text': f'{color.name} variant', 'color': color}
    )
    if img_created:
        print(f"[OK] Added image: {img_path} linked to {color.name}")
    elif not img.color:
        img.color = color
        img.save()
        print(f"[OK] Linked existing image to {color.name}")

print(f"\n[SUCCESS] Product B601 successfully added with {len(color_data)} colors and {len(sizes_to_use)} sizes!")
print(f"Total variants created: {len(color_data) * len(sizes_to_use)}")
