from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Booking, Contact


@receiver(post_save, sender=Booking)
def send_booking_notification_to_admin(sender, instance, created, **kwargs):
    """Gửi email thông báo đến admin khi có booking mới"""
    if created:  # Chỉ gửi khi booking được tạo
        try:
            # Lấy danh sách email admin
            admin_emails = [admin[1] for admin in settings.ADMINS]
            
            if not admin_emails:
                # Nếu không có ADMINS, dùng DEFAULT_FROM_EMAIL
                admin_emails = [settings.DEFAULT_FROM_EMAIL] if hasattr(settings, 'DEFAULT_FROM_EMAIL') else []
            
            if not admin_emails:
                print("⚠️ Không có email admin được cấu hình")
                return
            
            # Chuẩn bị dữ liệu email
            subject = f'🔔 Đặt lịch mới - {instance.customer_name} ({instance.get_package_name()})'
            
            context = {
                'booking': instance,
                'package_name': instance.package.get_name_display(),
                'package_price': instance.package.price,
                'package_duration': instance.package.duration,
                'site_name': settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'My Portfolio',
            }
            
            # Tạo email HTML
            html_message = f"""
            <html>
                <body style="font-family: Arial, sans-serif; direction: ltr;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 8px;">
                        <h2 style="color: #333; border-bottom: 3px solid #009603; padding-bottom: 10px;">📋 Thông Báo Đặt Lịch Mới</h2>
                        
                        <div style="background-color: #fff; padding: 20px; border-radius: 5px; margin-top: 20px;">
                            <h3 style="color: #009603;">Chi Tiết Khách Hàng</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; width: 150px;">👤 Tên khách hàng:</td>
                                    <td style="padding: 8px;">{instance.customer_name}</td>
                                </tr>
                                <tr style="background-color: #f5f5f5;">
                                    <td style="padding: 8px; font-weight: bold;">📧 Email:</td>
                                    <td style="padding: 8px;">{instance.customer_email}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">📱 Điện thoại:</td>
                                    <td style="padding: 8px;">{instance.customer_phone}</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div style="background-color: #fff; padding: 20px; border-radius: 5px; margin-top: 20px;">
                            <h3 style="color: #009603;">Chi Tiết Dịch Vụ</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; width: 150px;">📦 Gói dịch vụ:</td>
                                    <td style="padding: 8px;"><strong style="color: #009603; font-size: 16px;">{instance.package.get_name_display()}</strong></td>
                                </tr>
                                <tr style="background-color: #f5f5f5;">
                                    <td style="padding: 8px; font-weight: bold;">💰 Giá:</td>
                                    <td style="padding: 8px; font-size: 16px; color: #009603;"><strong>${instance.package.price}</strong></td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">⏱️ Thời lượng:</td>
                                    <td style="padding: 8px;">{instance.package.duration} giờ</td>
                                </tr>
                                <tr style="background-color: #f5f5f5;">
                                    <td style="padding: 8px; font-weight: bold;">📅 Ngày dự kiến:</td>
                                    <td style="padding: 8px;">{instance.scheduled_date.strftime('%d/%m/%Y')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">🕐 Ngày đặt:</td>
                                    <td style="padding: 8px;">{instance.booking_date.strftime('%d/%m/%Y %H:%M:%S')}</td>
                                </tr>
                                <tr style="background-color: #f5f5f5;">
                                    <td style="padding: 8px; font-weight: bold;">✅ Trạng thái:</td>
                                    <td style="padding: 8px;">
                                        <span style="background-color: #fff3cd; color: #856404; padding: 4px 8px; border-radius: 3px; font-weight: bold;">
                                            {instance.get_status_display()}
                                        </span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">🔑 ID Booking:</td>
                                    <td style="padding: 8px;"><code style="background-color: #f0f0f0; padding: 2px 6px; border-radius: 3px;">{instance.id}</code></td>
                                </tr>
                            </table>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px;">
                            <a href="http://127.0.0.1:8000/admin/portfolio/booking/{instance.id}/change/" 
                               style="background-color: #009603; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                                Xem Chi Tiết Trong Admin
                            </a>
                        </div>
                        
                        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                            <p>✉️ Đây là thông báo tự động từ hệ thống. Vui lòng không trả lời email này.</p>
                            <p>📌 Hãy đăng nhập vào admin panel để xem và quản lý các booking.</p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            # Gửi email
            send_mail(
                subject=subject,
                message=strip_tags(html_message),  # Nội dung text (fallback)
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=admin_emails,
                html_message=html_message,
                fail_silently=False,
            )
            
            print(f"✅ Đã gửi thông báo booking đến admin: {admin_emails}")
            
        except Exception as e:
            print(f"❌ Lỗi khi gửi email: {str(e)}")


@receiver(post_save, sender=Contact)
def send_contact_notification_to_admin(sender, instance, created, **kwargs):
    """Gửi email thông báo đến admin khi có tin nhắn liên hệ mới"""
    if created:  # Chỉ gửi khi contact message được tạo
        try:
            # Lấy danh sách email admin
            admin_emails = [admin[1] for admin in settings.ADMINS]
            
            if not admin_emails:
                # Nếu không có ADMINS, dùng DEFAULT_FROM_EMAIL
                admin_emails = [settings.DEFAULT_FROM_EMAIL] if hasattr(settings, 'DEFAULT_FROM_EMAIL') else []
            
            if not admin_emails:
                print("⚠️ Không có email admin được cấu hình")
                return
            
            # Chuẩn bị dữ liệu email
            subject = f'📧 Tin nhắn liên hệ mới từ {instance.name}'
            
            # Tạo email HTML
            html_message = f"""
            <html>
                <body style="font-family: Arial, sans-serif; direction: ltr;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 8px;">
                        <h2 style="color: #333; border-bottom: 3px solid #0066cc; padding-bottom: 10px;">📧 Tin Nhắn Liên Hệ Mới</h2>
                        
                        <div style="background-color: #fff; padding: 20px; border-radius: 5px; margin-top: 20px;">
                            <h3 style="color: #0066cc;">Thông Tin Người Gửi</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; width: 150px;">👤 Tên:</td>
                                    <td style="padding: 8px;"><strong>{instance.name}</strong></td>
                                </tr>
                                <tr style="background-color: #f5f5f5;">
                                    <td style="padding: 8px; font-weight: bold;">📧 Email:</td>
                                    <td style="padding: 8px;">
                                        <a href="mailto:{instance.email}" style="color: #0066cc; text-decoration: none;">
                                            {instance.email}
                                        </a>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold;">🕐 Thời gian gửi:</td>
                                    <td style="padding: 8px;">{instance.id} (ID Contact)</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div style="background-color: #fff; padding: 20px; border-radius: 5px; margin-top: 20px;">
                            <h3 style="color: #0066cc;">Nội Dung Tin Nhắn</h3>
                            <div style="background-color: #f0f7ff; padding: 15px; border-left: 4px solid #0066cc; border-radius: 4px; line-height: 1.6; color: #333;">
                                {instance.message.replace(chr(10), '<br>')}
                            </div>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px;">
                            <a href="http://127.0.0.1:8000/admin/portfolio/contact/{instance.id}/change/" 
                               style="background-color: #0066cc; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold; margin-right: 10px;">
                                Xem Chi Tiết Trong Admin
                            </a>
                            <a href="mailto:{instance.email}" 
                               style="background-color: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                                Trả Lời Email
                            </a>
                        </div>
                        
                        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                            <p>✉️ Đây là thông báo tự động từ hệ thống. Vui lòng không trả lời email này trực tiếp.</p>
                            <p>💬 Hãy đăng nhập vào admin panel để xem tất cả các tin nhắn liên hệ.</p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            # Gửi email
            send_mail(
                subject=subject,
                message=strip_tags(html_message),  # Nội dung text (fallback)
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=admin_emails,
                html_message=html_message,
                fail_silently=False,
            )
            
            print(f"✅ Đã gửi thông báo liên hệ đến admin: {admin_emails}")
            print(f"   Từ: {instance.name} <{instance.email}>")
            
        except Exception as e:
            print(f"❌ Lỗi khi gửi email liên hệ: {str(e)}")
