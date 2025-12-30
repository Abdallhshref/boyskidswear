"""
Script to cleanup categories and duplicates
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Product, Category

# Get categories
boys_cat = Category.objects.get(slug='kids-boys')
girls_cat = Category.objects.get(slug='kids-girls')

# 1. Handle B601 duplicate
try:
    bad_b601 = Product.objects.get(slug='b601')
    good_b601 = Product.objects.get(slug='hello-dino-set-b601')
    print(f"Found duplicate B601s. Deleting generic 'b601'...")
    bad_b601.delete()
    print("[OK] Deleted 'b601'")
except Product.DoesNotExist:
    print("No duplicate 'b601' found.")

# 2. Update B600 and B602 to Kids Boys
for slug in ['b600', 'b602']:
    try:
        p = Product.objects.get(slug=slug)
        if p.category != boys_cat:
            p.category = boys_cat
            p.save()
            print(f"[OK] Moved {p.name} ({slug}) to Kids Boys")
        else:
            print(f"{p.name} ({slug}) is already in Kids Boys")
    except Product.DoesNotExist:
        print(f"Product {slug} not found")

print("\n[DONE] Cleanup complete")
