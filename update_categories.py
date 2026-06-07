import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from portfolio.models import Category

# Xóa các category cũ
Category.objects.all().delete()

# Tạo 4 category mới
categories_data = [
    {'name': 'Thời trang', 'order': 1},
    {'name': 'Đời sống', 'order': 2},
    {'name': 'Phong cảnh', 'order': 3},
    {'name': 'Đám cưới', 'order': 4},
]

for data in categories_data:
    Category.objects.create(**data)

# In ra kết quả
print("✅ Đã tạo các category:")
for cat in Category.objects.all():
    print(f"  - {cat.name}")
