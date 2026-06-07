from django.db import models

class Profile(models.Model):

    name = models.CharField(max_length=100)

    bio = models.TextField()

    avatar = models.ImageField(upload_to='avatar/')

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Skill(models.Model):

    name = models.CharField(max_length=100)
    percent = models.IntegerField()
    image = models.ImageField(upload_to='skills/', blank=True, null=True, help_text='Hình ảnh đại diện cho kỹ năng')
    icon = models.CharField(max_length=100, blank=True, help_text='Tên icon Font Awesome (ví dụ: fa-camera) hoặc class CSS tùy chỉnh')
    description = models.TextField(blank=True, help_text='Mô tả ngắn cho kỹ năng này')
    order = models.IntegerField(default=0, help_text='Thứ tự hiển thị kỹ năng')

    class Meta:
        ordering = ['order', '-percent']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Model cho danh mục sản phẩm/dịch vụ"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Project(models.Model):

    title = models.CharField(max_length=100)

    description = models.TextField()

    image = models.ImageField(upload_to='projects/')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)

    def __str__(self):
        return self.title


class Blog(models.Model):

    title = models.CharField(max_length=200)

    content = models.TextField()

    image = models.ImageField(upload_to='blogs/')
    hero_image = models.ImageField(upload_to='blogs/hero/', blank=True, null=True, help_text='Ảnh hero hiển thị ở đầu trang chi tiết')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Contact(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    message = models.TextField()

    def __str__(self):
        return self.name


class SiteSetting(models.Model):
    site_title = models.CharField(max_length=200, default='My Site')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    footer_logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Logo cho footer')
    footer_heading = models.CharField(max_length=200, blank=True, help_text='Tiêu đề phần footer ở cột trái')
    footer_description = models.TextField(blank=True, help_text='Mô tả ngắn phần footer ở cột trái')
    
    # Thông tin cơ bản
    tagline = models.CharField(max_length=255, blank=True, help_text='Slogan/tagline của trang')
    description = models.TextField(blank=True, help_text='Mô tả trang web')
    footer_text = models.CharField(max_length=255, blank=True)
    copyright_text = models.CharField(max_length=255, blank=True, help_text='Văn bản copyright')

    # Thông tin liên hệ
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True, help_text='Địa chỉ công ty')
    
    # Giờ hoạt động
    opening_hours = models.TextField(blank=True, help_text='Giờ hoạt động (ví dụ: Mon-Fri: 9AM-6PM)')
    
    # Mạng xã hội
    facebook_url = models.URLField(blank=True, help_text='Link Facebook')
    twitter_url = models.URLField(blank=True, help_text='Link Twitter')
    youtube_url = models.URLField(blank=True, help_text='Link YouTube')
    instagram_url = models.URLField(blank=True, help_text='Link Instagram')
    linkedin_url = models.URLField(blank=True, help_text='Link LinkedIn')

    class Meta:
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_title


class Page(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    breadcrumb_title = models.CharField(max_length=100, blank=True, help_text='Tiêu đề nhỏ cho breadcrumb')
    meta_description = models.CharField(max_length=255, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True, help_text='Nội dung HTML của trang. Có thể dùng thẻ <p>, <strong>, <ul>, ...')
    featured_image = models.ImageField(upload_to='pages/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return self.title


class Hero(models.Model):
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=400, blank=True)
    image = models.ImageField(upload_to='hero/', blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.heading


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_items')
    featured = models.BooleanField(default=False, help_text='Đánh dấu ảnh này để hiển thị ở phần "Những bức ảnh nổi bật"')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or f'Image {self.pk}'


class Pricing(models.Model):
    PACKAGE_CHOICES = [
        ('basic', 'Cơ bản'),
        ('standard', 'Tiêu chuẩn'),
        ('premium', 'Mở rộng'),
        ('ultimate', 'Tối ưu'),
    ]
    
    name = models.CharField(max_length=100, choices=PACKAGE_CHOICES, unique=True)
    price = models.IntegerField()  # in USD
    duration = models.IntegerField()  # in hours
    description = models.TextField(blank=True)
    features = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f'{self.get_name_display()} - ${self.price}'


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('cancelled', 'Bị hủy'),
    ]
    
    package = models.ForeignKey(Pricing, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    booking_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.customer_name} - {self.package.get_name_display()}'
    
    def get_package_name(self):
        """Lấy tên gói dịch vụ"""
        return self.package.get_name_display()
    
    class Meta:
        ordering = ['-booking_date']


class AboutContent(models.Model):
    """Nội dung chính trang Giới thiệu"""
    main_title = models.CharField(max_length=300, default='Ghi lại những khoảnh khắc chạm đến trái tim bạn')
    main_description = models.TextField(default='Chúng tôi tạo ra những hình ảnh và video đầy cảm xúc, chuyên nghiệp và mang đậm phong cách riêng.')
    about_image = models.ImageField(upload_to='about/', blank=True, null=True, help_text='Ảnh chính trong phần Giới thiệu')
    video_url = models.URLField(blank=True, help_text='Link video YouTube (ví dụ: https://www.youtube.com/watch?v=...)')
    testimonial_title = models.CharField(max_length=200, blank=True, default='Khách hàng nói gì?', help_text='Tiêu đề phần testimonial trên trang About')
    testimonial_description = models.TextField(blank=True, default='Đánh giá chân thực từ những khách hàng đã trải nghiệm dịch vụ của chúng tôi.', help_text='Mô tả nhỏ bên dưới tiêu đề testimonial')
    
    class Meta:
        verbose_name_plural = "About Content"
    
    def __str__(self):
        return "Nội dung trang Giới thiệu"


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_handle = models.CharField(max_length=100, blank=True, help_text='Tài khoản @ hoặc mô tả thêm')
    quote = models.TextField()
    image = models.ImageField(upload_to='testimonial/', blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Testimonials'
    
    def __str__(self):
        return self.customer_name


class AboutFeature(models.Model):
    """Các điểm nổi bật trong trang Giới thiệu"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_image = models.ImageField(upload_to='about/', help_text='Ảnh icon cho điểm nổi bật')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "About Features"
    
    def __str__(self):
        return self.title


class TeamMember(models.Model):
    """Thành viên trong đội ngũ"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, help_text='Vị trí/chức vụ (ví dụ: Nhiếp ảnh gia, Đạo diễn)')
    image = models.ImageField(upload_to='team/', help_text='Ảnh của thành viên')
    
    # Social media links
    facebook_url = models.URLField(blank=True, help_text='Link Facebook profile')
    twitter_url = models.URLField(blank=True, help_text='Link Twitter profile')
    youtube_url = models.URLField(blank=True, help_text='Link YouTube channel')
    instagram_url = models.URLField(blank=True, help_text='Link Instagram profile')
    
    order = models.IntegerField(default=0, help_text='Thứ tự hiển thị')
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return self.name
