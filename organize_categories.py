"""
Script to create Kids Boys and Kids Girls categories and assign products
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product

# Create categories
boys_cat, boys_created = Category.objects.get_or_create(
    slug='kids-boys',
    defaults={'name': 'Kids Boys'}
)
print(f"[{'Created' if boys_created else 'Exists'}] Category: {boys_cat.name}")

girls_cat, girls_created = Category.objects.get_or_create(
    slug='kids-girls',
    defaults={'name': 'Kids Girls'}
)
print(f"[{'Created' if girls_created else 'Exists'}] Category: {girls_cat.name}")

# Assign products to Boys category
boys_slugs = [
    'hello-dino-set-b601',
    'panda-dreams-set-b604',
    'pilot-kids-awesome-set-b606',
]

for slug in boys_slugs:
    try:
        product = Product.objects.get(slug=slug)
        product.category = boys_cat
        product.save()
        print(f"  [OK] {product.name} -> Kids Boys")
    except Product.DoesNotExist:
        print(f"  [WARN] Product with slug '{slug}' not found")

# Assign products to Girls category  
girls_slugs = [
    'love-mom-butterfly-set-b605',
]

for slug in girls_slugs:
    try:
        product = Product.objects.get(slug=slug)
        product.category = girls_cat
        product.save()
        print(f"  [OK] {product.name} -> Kids Girls")
    except Product.DoesNotExist:
        print(f"  [WARN] Product with slug '{slug}' not found")

print("\n[DONE] Category assignment complete!")
