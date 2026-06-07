#!/usr/bin/env python
"""
Test script để kiểm tra hệ thống gửi email thông báo booking
Chạy: python manage.py shell < test_booking_notification.py
"""

from portfolio.models import Pricing, Booking
from django.utils import timezone
from datetime import datetime, timedelta

# Tạo gói dịch vụ nếu chưa có
pricing, created = Pricing.objects.get_or_create(
    name='basic',
    defaults={
        'price': 99,
        'duration': 2,
        'description': 'Gói cơ bản',
        'features': ['Tư vấn cơ bản', 'Email support'],
    }
)

print(f"✅ Gói dịch vụ: {pricing.get_name_display()} (${pricing.price})")

# Tạo booking test (sẽ trigger signal)
booking = Booking.objects.create(
    package=pricing,
    customer_name='Nguyễn Văn A',
    customer_email='customer@example.com',
    customer_phone='0123456789',
    scheduled_date=timezone.now().date() + timedelta(days=7),
    status='pending',
    notes='Test booking notification'
)

print(f"✅ Booking được tạo:")
print(f"   - ID: {booking.id}")
print(f"   - Khách: {booking.customer_name}")
print(f"   - Email: {booking.customer_email}")
print(f"   - Gói: {booking.get_package_name()}")
print(f"\n✅ Kiểm tra console để xem email thông báo đã được gửi")
