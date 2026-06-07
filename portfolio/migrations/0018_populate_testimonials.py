from django.db import migrations


def populate_testimonials(apps, schema_editor):
    AboutContent = apps.get_model('portfolio', 'AboutContent')
    Testimonial = apps.get_model('portfolio', 'Testimonial')

    about_content = AboutContent.objects.first()
    if about_content:
        about_content.testimonial_title = 'Khách hàng nói gì?'
        about_content.testimonial_description = 'Đánh giá chân thực từ những khách hàng đã trải nghiệm dịch vụ của chúng tôi.'
        about_content.save()

    testimonials = [
        {
            'customer_name': 'Andrew Filder',
            'customer_handle': '@filder_muko',
            'quote': 'Dịch vụ rất chuyên nghiệp và kết quả vượt mong đợi.',
            'order': 1,
        },
        {
            'customer_name': 'David Guetta',
            'customer_handle': '@filder_muko',
            'quote': 'Đội ngũ rất thân thiện, tôi cảm thấy thoải mái trong suốt buổi chụp.',
            'order': 2,
        },
        {
            'customer_name': 'Bebe Rexha',
            'customer_handle': '@filder_muko',
            'quote': 'Hình ảnh được xử lý kỹ lưỡng, màu sắc đẹp và tôi rất hài lòng.',
            'order': 3,
        },
        {
            'customer_name': 'Adam Levine',
            'customer_handle': '@filder_muko',
            'quote': 'Sản phẩm cuối cùng rất chuyên nghiệp, tôi rất hài lòng với dịch vụ.',
            'order': 4,
        },
    ]

    for data in testimonials:
        Testimonial.objects.get_or_create(
            customer_name=data['customer_name'],
            customer_handle=data['customer_handle'],
            quote=data['quote'],
            defaults={'order': data['order']},
        )


def reverse_populate_testimonials(apps, schema_editor):
    Testimonial = apps.get_model('portfolio', 'Testimonial')
    Testimonial.objects.filter(customer_name__in=[
        'Andrew Filder', 'David Guetta', 'Bebe Rexha', 'Adam Levine'
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0017_testimonial_aboutcontent_testimonial_description_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_testimonials, reverse_populate_testimonials),
    ]
