# Generated migration to populate default About data

from django.db import migrations

def populate_about_data(apps, schema_editor):
    """Populate default About content and features"""
    AboutContent = apps.get_model('portfolio', 'AboutContent')
    AboutFeature = apps.get_model('portfolio', 'AboutFeature')
    
    # Create default AboutContent if not exists
    about_content, created = AboutContent.objects.get_or_create(
        pk=1,
        defaults={
            'main_title': 'Ghi lại những khoảnh khắc chạm đến trái tim bạn',
            'main_description': 'Chúng tôi tạo ra những hình ảnh và video đầy cảm xúc, chuyên nghiệp và mang đậm phong cách riêng.',
            'video_url': 'https://www.youtube.com/watch?v=hxADTEJalRw',
        }
    )
    
    # Create default AboutFeatures
    features_data = [
        {
            'title': 'Chuyên nghiệp',
            'description': 'Đội ngũ giàu kinh nghiệm, luôn đặt chất lượng và tinh thần chuyên nghiệp lên hàng đầu.',
            'order': 1
        },
        {
            'title': 'Tiếp cận cá nhân',
            'description': 'Mỗi dự án được thiết kế riêng theo phong cách và mong muốn của khách hàng.',
            'order': 2
        },
        {
            'title': 'Lịch trình linh hoạt',
            'description': 'Chúng tôi hỗ trợ đặt lịch linh hoạt, phù hợp với thời gian của bạn.',
            'order': 3
        },
        {
            'title': 'Kinh nghiệm',
            'description': 'Chúng tôi có kinh nghiệm đa dạng trong nhiều loại hình chụp ảnh và quay phim.',
            'order': 4
        },
    ]
    
    for feature_data in features_data:
        AboutFeature.objects.get_or_create(
            title=feature_data['title'],
            defaults=feature_data
        )

def reverse_about_data(apps, schema_editor):
    """Reverse operation"""
    AboutContent = apps.get_model('portfolio', 'AboutContent')
    AboutFeature = apps.get_model('portfolio', 'AboutFeature')
    AboutContent.objects.all().delete()
    AboutFeature.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0013_aboutcontent_aboutfeature'),
    ]

    operations = [
        migrations.RunPython(populate_about_data, reverse_about_data),
    ]
