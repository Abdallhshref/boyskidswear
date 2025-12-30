"""
Script to update B604 product images
Run with: python update_b604_images.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Product, ProductImage

# Get B604 product
try:
    product = Product.objects.get(slug='panda-dreams-set-b604')
    
    # Update main image
    product.main_image = 'products/B604/pink_1.jpg'
    product.save()
    print(f"[OK] Updated main image for {product.name}")
    
    # Add gallery images
    gallery_images = [
        {'path': 'products/B604/white_1.jpg', 'alt': 'White and Black variant front view'},
        {'path': 'products/B604/blue_1.jpg', 'alt': 'Sky Blue and Black variant side view'},
        {'path': 'products/B604/pink_2.jpg', 'alt': 'Pink and Black variant back view'},
        {'path': 'products/B604/white_2.jpg', 'alt': 'White and Black variant back view'},
    ]
    
    for img_data in gallery_images:
        img, created = ProductImage.objects.get_or_create(
            product=product,
            image=img_data['path'],
            defaults={'alt_text': img_data['alt']}
        )
        if created:
            print(f"[OK] Added gallery image: {img_data['path']}")
    
    print(f"\n[SUCCESS] All images updated for {product.name}!")
    
except Product.DoesNotExist:
    print("[ERROR] Product B604 not found!")
