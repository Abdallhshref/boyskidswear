"""
Script to add B611 product to the database
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
    slug='brilliant-ideas-hoodie-set-b611',
    defaults={
        'name': 'Brilliant Ideas Hoodie Set B611',
        'description': 'Stylish "You have a brain full of brilliant ideas" hoodie set featuring a comfortable hoodie with tie-dye sleeves and matching pants with knee patches. Perfect for everyday wear, playtime, or casual outings. Made with soft, breathable fabric for your little one\'s comfort.',
        'category': category,
        'base_price': Decimal('480.00'),
        'main_image': 'products/B611/yellow_main.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# Define colors with gradient (top, pants)
color_data = [
    {'name': 'Yellow & Teal', 'hex': '#FFD700,#4682B4', 'img': 'yellow_main.jpg'},
    {'name': 'Sky Blue & Navy', 'hex': '#87CEEB,#191970', 'img': 'skyblue.jpg'},
    {'name': 'Beige & Brown', 'hex': '#F5F5DC,#8B4513', 'img': 'beige.jpg'},
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
    
    img_path = f'products/B611/{color_info["img"]}'
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        image=img_path,
        defaults={'alt_text': f'{color.name} variant', 'color': color}
    )
    if img_created:
        print(f"[OK] Added image: {img_path} linked to {color.name}")

print(f"\n[SUCCESS] Product B611 added with {len(color_data)} colors!")
