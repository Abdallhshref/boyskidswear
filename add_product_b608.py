"""
Script to add B608 product to the database
Run with: python add_product_b608.py
"""

import os
import django
from decimal import Decimal

# Setup Django
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
    slug='social-bunny-set-b608',
    defaults={
        'name': 'Social Bunny Set B608',
        'description': 'Adorable "Social" bunny themed baby outfit set featuring a comfortable sweatshirt with ruffle details and cute bunny ears print, paired with matching ruffle-detail pants. Perfect for everyday wear, playtime, or casual outings. Made with soft, breathable fabric for your little one\'s comfort.',
        'category': category,
        'base_price': Decimal('450.00'),
        'main_image': 'products/B608/coral_main.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# Define colors with gradient (top, pants)
color_data = [
    {'name': 'Coral & Navy', 'hex': '#FF7F7F,#1C1C3C', 'img': 'coral_main.jpg'},
    {'name': 'Sky Blue & Hot Pink', 'hex': '#87CEEB,#FF69B4', 'img': 'skyblue.jpg'},
    {'name': 'Lavender', 'hex': '#DDA0DD,#DDA0DD', 'img': 'lavender.jpg'},
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
    color, color_created = Color.objects.get_or_create(
        name=color_info['name'],
        defaults={'hex_code': color_info['hex']}
    )
    
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
    img_path = f'products/B608/{color_info["img"]}'
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

print(f"\n[SUCCESS] Product B608 successfully added with {len(color_data)} colors and {len(sizes_to_use)} sizes!")
print(f"Total variants created: {len(color_data) * len(sizes_to_use)}")
