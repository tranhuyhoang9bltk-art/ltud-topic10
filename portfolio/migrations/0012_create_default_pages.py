# Generated migration to create default pages

from django.db import migrations

def create_default_pages(apps, schema_editor):
    """Create default pages for all theme pages"""
    Page = apps.get_model('portfolio', 'Page')
    
    pages_data = [
        {
            'slug': 'about',
            'title': 'Giới thiệu',
            'breadcrumb_title': 'Giới thiệu',
            'meta_description': 'Trang giới thiệu về dịch vụ chụp ảnh và quay phim chuyên nghiệp',
            'meta_keywords': 'giới thiệu, dịch vụ, chụp ảnh, quay phim',
            'content': '<p>Nội dung giới thiệu sẽ được hiển thị từ đây...</p>'
        },
        {
            'slug': 'services',
            'title': 'Dịch Vụ',
            'breadcrumb_title': 'Dịch vụ',
            'meta_description': 'Các dịch vụ chụp ảnh và quay phim của chúng tôi',
            'meta_keywords': 'dịch vụ, chụp ảnh, quay phim, video',
            'content': '<p>Danh sách dịch vụ sẽ được quản lý từ danh mục Services trong admin...</p>'
        },
        {
            'slug': 'pricing',
            'title': 'Bảng Giá',
            'breadcrumb_title': 'Bảng giá',
            'meta_description': 'Bảng giá dịch vụ chụp ảnh và quay phim',
            'meta_keywords': 'giá, bảng giá, chi phí, dịch vụ',
            'content': '<p>Bảng giá sẽ được quản lý từ danh mục Pricing trong admin...</p>'
        },
        {
            'slug': 'portfolio',
            'title': 'Danh Sách Dự Án',
            'breadcrumb_title': 'Dự án',
            'meta_description': 'Xem các dự án đã thực hiện của chúng tôi',
            'meta_keywords': 'dự án, portfolio, công việc, chứng chỉ',
            'content': '<p>Danh sách dự án sẽ được quản lý từ danh mục Project trong admin...</p>'
        },
        {
            'slug': 'gallery',
            'title': 'Thư Viện Ảnh',
            'breadcrumb_title': 'Thư viện',
            'meta_description': 'Thư viện ảnh và video các công việc chúng tôi đã thực hiện',
            'meta_keywords': 'thư viện, ảnh, video, gallery, tác phẩm',
            'content': '<p>Thư viện ảnh sẽ được quản lý từ danh mục Gallery trong admin...</p>'
        },
        {
            'slug': 'blog',
            'title': 'Bài Viết',
            'breadcrumb_title': 'Bài viết',
            'meta_description': 'Bài viết, tin tức và kinh nghiệm chụp ảnh',
            'meta_keywords': 'blog, bài viết, tin tức, kinh nghiệm',
            'content': '<p>Danh sách bài viết sẽ được quản lý từ danh mục Blog trong admin...</p>'
        },
        {
            'slug': 'categories',
            'title': 'Danh Mục',
            'breadcrumb_title': 'Danh mục',
            'meta_description': 'Danh mục dự án và dịch vụ',
            'meta_keywords': 'danh mục, phân loại, chủ đề',
            'content': '<p>Danh mục sẽ được quản lý từ danh mục Category trong admin...</p>'
        },
        {
            'slug': 'contact',
            'title': 'Liên Hệ',
            'breadcrumb_title': 'Liên hệ',
            'meta_description': 'Liên hệ với chúng tôi để tư vấn dịch vụ',
            'meta_keywords': 'liên hệ, tư vấn, gửi tin nhắn, email',
            'content': '<p>Form liên hệ sẽ hiển thị ở đây...</p>'
        },
        {
            'slug': 'profile',
            'title': 'Hồ Sơ',
            'breadcrumb_title': 'Hồ sơ',
            'meta_description': 'Thông tin cá nhân và kỹ năng',
            'meta_keywords': 'hồ sơ, thông tin, kỹ năng, cv',
            'content': '<p>Thông tin hồ sơ sẽ được quản lý từ danh mục Profile trong admin...</p>'
        },
    ]
    
    for page_data in pages_data:
        Page.objects.get_or_create(
            slug=page_data['slug'],
            defaults=page_data
        )

def delete_pages(apps, schema_editor):
    """Reverse operation"""
    Page = apps.get_model('portfolio', 'Page')
    Page.objects.filter(slug__in=[
        'about', 'services', 'pricing', 'portfolio', 'gallery', 
        'blog', 'categories', 'contact', 'profile'
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0011_page'),
    ]

    operations = [
        migrations.RunPython(create_default_pages, delete_pages),
    ]
