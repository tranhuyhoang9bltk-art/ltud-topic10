from django.db import migrations


def create_default_pricing(apps, schema_editor):
    Pricing = apps.get_model('portfolio', 'Pricing')

    default_packages = [
        {
            'name': 'basic',
            'price': 99,
            'duration': 1,
            'description': 'Gói cơ bản dành cho chụp nhanh, ít hậu kỳ.',
            'features': ['Tối đa 30 ảnh', 'Không chỉnh sửa ảnh', 'Không trang điểm', 'Không hỗ trợ stylist'],
        },
        {
            'name': 'standard',
            'price': 199,
            'duration': 2,
            'description': 'Gói tiêu chuẩn phù hợp cho nhu cầu cơ bản.',
            'features': ['Tối đa 30 ảnh', 'Chỉnh sửa tối thiểu', 'Không trang điểm', 'Không hỗ trợ stylist'],
        },
        {
            'name': 'premium',
            'price': 299,
            'duration': 3,
            'description': 'Gói mở rộng với thêm thời gian và hậu kỳ.',
            'features': ['Tối đa 30 ảnh', 'Chỉnh sửa hình cơ bản', 'Trang điểm cơ bản', 'Hỗ trợ stylist'],
        },
        {
            'name': 'ultimate',
            'price': 399,
            'duration': 5,
            'description': 'Gói tối ưu cho sự kiện và sản phẩm cao cấp.',
            'features': ['Tối đa 30 ảnh', 'Chỉnh sửa full', 'Trang điểm và stylist', 'Hậu kỳ chuyên sâu'],
        },
    ]

    for package in default_packages:
        Pricing.objects.get_or_create(
            name=package['name'],
            defaults={
                'price': package['price'],
                'duration': package['duration'],
                'description': package['description'],
                'features': package['features'],
            }
        )


def remove_default_pricing(apps, schema_editor):
    Pricing = apps.get_model('portfolio', 'Pricing')
    Pricing.objects.filter(name__in=['basic', 'standard', 'premium', 'ultimate']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_pricing_booking'),
    ]

    operations = [
        migrations.RunPython(create_default_pricing, remove_default_pricing),
    ]
