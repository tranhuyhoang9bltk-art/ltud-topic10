from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import *

# Register new theme models
from .models import SiteSetting, Hero, Service, Gallery, Pricing, Booking, Category

# ========== CUSTOM ADMIN SITE ==========
class CustomAdminSite(admin.AdminSite):
    site_header = "Phozogy Portfolio Admin"
    site_title = "Portfolio Admin"
    index_title = "📊 Dashboard Quản Lý"
    index_template = 'admin/index.html'
    
    def index(self, request, extra_context=None):
        """Custom admin index with booking notifications"""
        from django.db.models import Count, Q
        from datetime import datetime, timedelta
        
        extra_context = extra_context or {}
        
        # Pending bookings (chưa thanh toán)
        pending_bookings = Booking.objects.filter(status='pending').order_by('-booking_date')[:5]
        pending_count = Booking.objects.filter(status='pending').count()
        
        # Recent bookings (24 giờ gần đây)
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        recent_bookings = Booking.objects.filter(booking_date__gte=yesterday).order_by('-booking_date')[:5]
        recent_count = recent_bookings.count()
        
        # Upcoming bookings (7 ngày tới)
        next_week = today.date() + timedelta(days=7)
        upcoming_bookings = Booking.objects.filter(scheduled_date__range=[today.date(), next_week]).order_by('scheduled_date')[:5]
        upcoming_count = upcoming_bookings.count()
        
        # Statistics
        total_bookings = Booking.objects.count()
        total_revenue = sum(b.package.price for b in Booking.objects.filter(status='paid'))
        
        extra_context.update({
            'pending_bookings': pending_bookings,
            'pending_count': pending_count,
            'recent_bookings': recent_bookings,
            'recent_count': recent_count,
            'upcoming_bookings': upcoming_bookings,
            'upcoming_count': upcoming_count,
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
        })
        
        return super().index(request, extra_context=extra_context)

# Create custom admin site instance
admin_site = CustomAdminSite()


# ========== PROFILE ADMIN ==========
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'profile_avatar')
    search_fields = ('name', 'email')
    
    fieldsets = (
        ('👤 Thông Tin Cơ Bản', {
            'fields': ('name', 'email', 'phone')
        }),
        ('📸 Avatar', {
            'fields': ('avatar',)
        }),
        ('📝 Tiểu sử', {
            'fields': ('bio',)
        }),
    )
    
    def profile_avatar(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" style="max-height: 50px; border-radius: 50%;" />'
        return '—'
    profile_avatar.short_description = 'Avatar'
    profile_avatar.allow_tags = True


admin_site.register(Profile, ProfileAdmin)


# ========== SKILL ADMIN ==========
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'skill_image_preview', 'icon_preview', 'order', 'skill_bar', 'description_preview')
    list_editable = ('percent', 'order')
    search_fields = ('name', 'description')
    ordering = ('order', '-percent', 'name')
    list_per_page = 25
    fieldsets = (
        ('💼 Kỹ Năng', {
            'fields': ('name', 'percent', 'image', 'icon', 'description', 'order')
        }),
    )
    
    def skill_bar(self, obj):
        percentage = obj.percent
        return f'<div style="background-color: #e9ecef; border-radius: 10px; width: 120px; height: 14px; overflow: hidden;"><div style="background-color: #009603; height: 100%; width: {percentage}%;"></div></div>'
    skill_bar.short_description = 'Mức độ'
    skill_bar.allow_tags = True

    def skill_image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; border-radius: 6px;" />'
        return '—'
    skill_image_preview.short_description = 'Ảnh'
    skill_image_preview.allow_tags = True

    def icon_preview(self, obj):
        if obj.icon:
            return f'<i class="fa {obj.icon}" style="font-size:18px;color:#009603"></i> {obj.icon}'
        return '—'
    icon_preview.short_description = 'Icon'
    icon_preview.allow_tags = True

    def description_preview(self, obj):
        if obj.description:
            return obj.description[:70] + ('...' if len(obj.description) > 70 else '')
        return '—'
    description_preview.short_description = 'Mô tả'


admin_site.register(Skill, SkillAdmin)


# ========== PROJECT ADMIN ==========
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_name', 'project_image')
    search_fields = ('title', 'description', 'category__name')
    list_filter = ('category',)
    
    fieldsets = (
        ('📋 Thông Tin Dự Án', {
            'fields': ('title', 'description', 'category')
        }),
        ('🖼️ Hình Ảnh', {
            'fields': ('image',)
        }),
    )
    
    def project_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; border-radius: 3px;" />'
        return '—'
    project_image.short_description = 'Hình ảnh'
    project_image.allow_tags = True
    
    def category_name(self, obj):
        if obj.category:
            return obj.category.name
        return '—'
    category_name.short_description = 'Danh mục'


admin_site.register(Project, ProjectAdmin)


# ========== BLOG ADMIN ==========
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog_image', 'blog_hero', 'created_at', 'word_count')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('📝 Nội Dung', {
            'fields': ('title', 'content')
        }),
        ('🖼️ Hình Ảnh', {
            'fields': ('image', 'hero_image')
        }),
        ('⏰ Ngày', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def blog_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; border-radius: 3px;" />'
        return '—'
    blog_image.short_description = 'Hình ảnh'
    blog_image.allow_tags = True
    
    def blog_hero(self, obj):
        if getattr(obj, 'hero_image', None):
            return f'<img src="{obj.hero_image.url}" style="max-height: 50px; border-radius: 3px;" />'
        return '—'
    blog_hero.short_description = 'Hero'
    blog_hero.allow_tags = True
    
    def word_count(self, obj):
        count = len(obj.content.split())
        return f'{count} từ'
    word_count.short_description = 'Số từ'


admin_site.register(Blog, BlogAdmin)


# ========== SITE SETTINGS ADMIN ==========
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'email', 'phone')
    
    fieldsets = (
        ('🌐 Thông Tin Trang Web', {
            'fields': ('site_title', 'tagline', 'description', 'logo', 'footer_logo')
        }),
        ('📧 Thông Tin Liên Hệ', {
            'fields': ('email', 'phone', 'address', 'opening_hours')
        }),
        ('📝 Nội Dung Footer', {
            'fields': ('footer_heading', 'footer_description', 'footer_text', 'copyright_text')
        }),
        ('🔗 Mạng Xã Hội', {
            'fields': ('facebook_url', 'twitter_url', 'youtube_url', 'instagram_url', 'linkedin_url'),
            'description': 'Thêm link đến các trang mạng xã hội của bạn'
        }),
    )
    
    def has_add_permission(self, request):
        """Chỉ cho phép 1 record SiteSetting"""
        return not SiteSetting.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Không cho phép xóa"""
        return False


admin_site.register(SiteSetting, SiteSettingAdmin)


# ========== HERO ADMIN ==========
class HeroAdmin(admin.ModelAdmin):
    list_display = ('heading', 'order', 'preview_image')
    list_editable = ('order',)
    search_fields = ('heading', 'subheading')
    
    fieldsets = (
        ('📋 Nội Dung', {
            'fields': ('heading', 'subheading')
        }),
        ('🖼️ Hình Ảnh', {
            'fields': ('image',)
        }),
        ('⚙️ Cài Đặt', {
            'fields': ('order',)
        }),
    )
    
    def preview_image(self, obj):
        if obj.image:
            return '✅ Có'
        return '❌ Không'
    preview_image.short_description = 'Hình ảnh'


admin_site.register(Hero, HeroAdmin)


# ========== SERVICE ADMIN ==========
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'icon_preview')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    
    fieldsets = (
        ('📋 Nội Dung', {
            'fields': ('title', 'description')
        }),
        ('🎨 Thiết Kế', {
            'fields': ('icon',),
            'description': 'Tên icon Font Awesome (ví dụ: fa-camera, fa-cog)'
        }),
        ('⚙️ Cài Đặt', {
            'fields': ('order',)
        }),
    )
    
    def icon_preview(self, obj):
        if obj.icon:
            return f'<i class="fa {obj.icon}"></i> {obj.icon}'
        return '—'
    icon_preview.short_description = 'Icon'
    icon_preview.allow_tags = True


admin_site.register(Service, ServiceAdmin)


# ========== PAGE ADMIN ==========
class PageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'updated_at')
    search_fields = ('slug', 'title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('📌 Nội dung trang', {
            'fields': ('slug', 'title', 'breadcrumb_title', 'meta_description', 'meta_keywords', 'featured_image', 'content')
        }),
    )

admin_site.register(Page, PageAdmin)


# ========== GALLERY ADMIN ==========
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'order', 'gallery_preview')
    list_editable = ('category', 'featured', 'order',)
    search_fields = ('title', 'category__name')
    list_filter = ('category', 'featured')
    
    fieldsets = (
        ('🖼️ Thông Tin', {
            'fields': ('title', 'image', 'category', 'featured')
        }),
        ('⚙️ Cài Đặt', {
            'fields': ('order',)
        }),
    )
    
    def gallery_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px;" />'
        return '—'
    gallery_preview.short_description = 'Xem trước'
    gallery_preview.allow_tags = True


admin_site.register(Gallery, GalleryAdmin)


# ========== CATEGORY ADMIN ==========
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'category_preview')
    list_editable = ('order',)
    search_fields = ('name', 'description')
    
    fieldsets = (
        ('📋 Thông tin', {
            'fields': ('name', 'description')
        }),
        ('🖼️ Hình ảnh', {
            'fields': ('image',)
        }),
        ('⚙️ Cài đặt', {
            'fields': ('order',)
        }),
    )
    
    def category_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; border-radius: 3px;" />'
        return '—'
    category_preview.short_description = 'Xem trước'
    category_preview.allow_tags = True


admin_site.register(Category, CategoryAdmin)


# ========== CONTACT ADMIN ==========
class ContactAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'contact_name', 'contact_email', 'message_preview', 'reply_btn')
    list_filter = ('name', 'email')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('id', 'name', 'email', 'message')
    
    fieldsets = (
        ('Thông tin liên hệ', {
            'fields': ('id', 'name', 'email')
        }),
        ('Nội dung', {
            'fields': ('message',)
        }),
    )
    
    def has_add_permission(self, request):
        """Không cho phép thêm contact từ admin"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Chỉ cho phép xem, không cho phép sửa"""
        return False if obj else True
    
    def contact_id(self, obj):
        return f'#{obj.id}'
    contact_id.short_description = 'ID'
    
    def contact_name(self, obj):
        return obj.name
    contact_name.short_description = 'Tên'
    
    def contact_email(self, obj):
        return f'<a href="mailto:{obj.email}">{obj.email}</a>'
    contact_email.short_description = 'Email'
    contact_email.allow_tags = True
    
    def message_preview(self, obj):
        preview = obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
        return preview.replace('\n', ' ')
    message_preview.short_description = 'Nội dung'
    
    def reply_btn(self, obj):
        return f'<a href="mailto:{obj.email}?subject=Re: Your Contact Message" class="button">Trả lời</a>'
    reply_btn.short_description = 'Hành động'
    reply_btn.allow_tags = True


admin_site.register(Contact, ContactAdmin)


# ========== BOOKING & PRICING ADMIN ==========
class PricingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'features_preview')
    list_editable = ('price', 'duration')
    list_filter = ('name', 'price', 'duration')
    search_fields = ('name', 'description')
    ordering = ('price',)
    fieldsets = (
        ('Thông tin gói', {
            'fields': ('name', 'price', 'duration', 'description', 'features')
        }),
    )
    
    def features_preview(self, obj):
        if obj.features:
            return ', '.join(obj.features[:3]) + ('...' if len(obj.features) > 3 else '')
        return '—'
    features_preview.short_description = 'Tính năng'


class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'customer_name', 'customer_email', 'package_name', 'booking_date', 'scheduled_date', 'status_badge')
    list_filter = ('status', 'booking_date', 'scheduled_date', 'package')
    search_fields = ('customer_name', 'customer_email', 'customer_phone', 'transaction_id')
    readonly_fields = ('booking_date', 'id')
    date_hierarchy = 'booking_date'
    
    fieldsets = (
        ('Thông tin khách hàng', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Thông tin dịch vụ', {
            'fields': ('package', 'scheduled_date', 'notes')
        }),
        ('Thông tin thanh toán', {
            'fields': ('status', 'transaction_id', 'booking_date', 'id')
        }),
    )
    
    def booking_id(self, obj):
        return f'#{obj.id}'
    booking_id.short_description = 'ID'
    
    def package_name(self, obj):
        return obj.package.get_name_display()
    package_name.short_description = 'Gói dịch vụ'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FFC107',   # Vàng
            'paid': '#28A745',      # Xanh lá
            'cancelled': '#DC3545', # Đỏ
        }
        color = colors.get(obj.status, '#999')
        return f'<span style="background-color: {color}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{obj.get_status_display()}</span>'
    status_badge.short_description = 'Trạng thái'
    status_badge.allow_tags = True


admin_site.register(Pricing, PricingAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)


# ========== ABOUT PAGE ADMIN ==========
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ('display_title',)
    fieldsets = (
        ('📝 Tiêu Đề và Mô Tả Chính', {
            'fields': ('main_title', 'main_description')
        }),
        ('🖼️ Ảnh Chính', {
            'fields': ('about_image',)
        }),
        ('🎥 Video', {
            'fields': ('video_url',),
            'description': 'Link video YouTube từ phần "Giới thiệu". Ví dụ: https://www.youtube.com/watch?v=...'
        }),
        ('💬 Testimonial Section', {
            'fields': ('testimonial_title', 'testimonial_description'),
            'description': 'Tiêu đề và mô tả cho khu vực đánh giá khách hàng ở trang Giới thiệu'
        }),
    )
    
    def has_add_permission(self, request):
        """Chỉ cho phép 1 record AboutContent"""
        return not AboutContent.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Không cho phép xóa"""
        return False
    
    def display_title(self, obj):
        return "⚙️ Cấu hình nội dung trang Giới thiệu"
    display_title.short_description = 'Cài đặt'


class AboutFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'preview_icon')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    
    fieldsets = (
        ('📋 Tiêu Đề & Mô Tả', {
            'fields': ('title', 'description')
        }),
        ('🖼️ Icon Ảnh', {
            'fields': ('icon_image',)
        }),
        ('⚙️ Thứ Tự Hiển Thị', {
            'fields': ('order',)
        }),
    )
    
    def preview_icon(self, obj):
        if obj.icon_image:
            return f'<img src="{obj.icon_image.url}" style="max-height: 40px; border-radius: 3px;" />'
        return '—'
    preview_icon.short_description = 'Icon'
    preview_icon.allow_tags = True


admin_site.register(AboutContent, AboutContentAdmin)
admin_site.register(AboutFeature, AboutFeatureAdmin)


# ========== TESTIMONIAL ADMIN ==========
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_handle', 'order', 'testimonial_image')
    list_editable = ('order',)
    search_fields = ('customer_name', 'customer_handle', 'quote')
    fieldsets = (
        ('👤 Thông Tin Khách Hàng', {
            'fields': ('customer_name', 'customer_handle')
        }),
        ('💬 Nội dung phản hồi', {
            'fields': ('quote',)
        }),
        ('🖼️ Ảnh', {
            'fields': ('image',),
            'description': 'Ảnh đại diện khách hàng hiển thị trong testimonial.'
        }),
        ('⚙️ Thứ tự', {
            'fields': ('order',)
        }),
    )
    
    def testimonial_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; border-radius: 50%;" />'
        return '—'
    testimonial_image.short_description = 'Ảnh'
    testimonial_image.allow_tags = True

admin_site.register(Testimonial, TestimonialAdmin)


# ========== TEAM MEMBER ADMIN ==========
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'team_avatar', 'social_links_preview')
    list_editable = ('order',)
    search_fields = ('name', 'position')
    
    fieldsets = (
        ('👤 Thông Tin Thành Viên', {
            'fields': ('name', 'position')
        }),
        ('📸 Ảnh', {
            'fields': ('image',)
        }),
        ('🔗 Mạng Xã Hội', {
            'fields': ('facebook_url', 'twitter_url', 'youtube_url', 'instagram_url'),
            'description': 'Thêm link đến các trang mạng xã hội của thành viên'
        }),
        ('⚙️ Cài Đặt', {
            'fields': ('order',)
        }),
    )
    
    def team_avatar(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; border-radius: 50%;" />'
        return '—'
    team_avatar.short_description = 'Ảnh'
    team_avatar.allow_tags = True
    
    def social_links_preview(self, obj):
        links = []
        if obj.facebook_url:
            links.append('📘')
        if obj.twitter_url:
            links.append('🐦')
        if obj.youtube_url:
            links.append('▶️')
        if obj.instagram_url:
            links.append('📷')
        return ' '.join(links) if links else '—'
    social_links_preview.short_description = 'Mạng xã hội'


admin_site.register(TeamMember, TeamMemberAdmin)
