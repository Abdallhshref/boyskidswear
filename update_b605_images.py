"""
Script to update B605 product images
Run with: python update_b605_images.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Product, ProductImage

# Get B605 product
try:
    product = Product.objects.get(slug='love-mom-butterfly-set-b605')
    
    # Update main image
    product.main_image = 'products/B605/lavender_main.jpg'
    product.save()
    print(f"[OK] Updated main image for {product.name}")
    
    # Add gallery images
    gallery_images = [
        {'path': 'products/B605/skyblue.jpg', 'alt': 'Sky Blue and Hot Pink variant'},
        {'path': 'products/B605/peach.jpg', 'alt': 'Peach and Turquoise variant'},
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
    print("[ERROR] Product B605 not found!")
